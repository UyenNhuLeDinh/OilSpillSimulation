import logging
import toml
from .mesh import Mesh
from .cells import *
from .simulation import Simulation

logger = logging.getLogger(__name__)

def log_summary(config_file, oil_distribution_history):
    """ 
    Log the summary of oil distribution in fishing grounds over time. 

    Parameters: 
    - config_file (str): Configuration file path. 
    - oil_distribution_history (list): List of oil distribution at different time steps. 

    Returns:
    - None 

    Exceptions: 
    - FileNotFoundError: Happens if the configuration files are not found.
    - Exception: Any errors happenign during the logging 
    """
    try:
        # Load configuration from TOML file:
        config = toml.load(config_file)
        mesh = Mesh(config['Settings']['mesh_path'])

        # Get fishing ground area from config:
        fishground = {
            'x_min': config['FishingGround']['x_range'][0],
            'x_max': config['FishingGround']['x_range'][1],
            'y_min': config['FishingGround']['y_range'][0],
            'y_max': config['FishingGround']['y_range'][1]
        }
        
        # Find the cell indices within the fishing grounds:
        cells_in_fish_ground = []
        for cell in mesh._cells_instances:
            for pts in cell._pointIDs:
                coord = mesh._points[pts]
                if (fishground['x_min'] <= coord[0] <= fishground['x_max'] and
                    fishground['y_min'] <= coord[1] <= fishground['y_max']):
                    cells_in_fish_ground.append(cell._idx)
                
        # Log amount of oil in the fishing ground over time:
        logger.info("Oil Distribution in Fishing Grounds Over Time:")
        for step, oil_distribution in enumerate(oil_distribution_history):
            total_oil_in_fishground = sum(oil_distribution.get(cell_index, 0.0) for cell_index in cells_in_fish_ground)
            logger.info(f"Time step {step}: Oil in Fishing Ground = {total_oil_in_fishground}")
        
    except FileNotFoundError:
        logger.error(f"Error: File '{config_file}' not found.")
    except Exception as e:
        logger.error(f"Error logging summary: {e}")

                