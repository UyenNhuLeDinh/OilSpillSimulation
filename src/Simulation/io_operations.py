import toml
import json

def read_config_file(filename):
    """
    Read simulation parameters from a TOML configuration file.

    Params:
        filename (str): Path to the TOML configuration file.
        
    Returns:
    dict: Dictionary containing simulation parameters.
    
    Raises:
    FileNotFoundError: If the specified file does not exist.
    ValueError: If the TOML file has inconsistent or missing entries.
    """
    try: 
        with open(filename, "r") as file:
            config = toml.load(file)
    
        # Verify the structure and required fields in config:
        required_input = {
            'Settings' : ['mesh_path','tStart', 'tEnd', 'num_steps'],
            'FishingGround' : ['x_range', 'y_range'],
            'IO' : ['logName', 'writeFrequency', 'restartFile']
        }
        for section, keys in required_input.items():
            if section not in config or not all(key in config[section] for key in keys):
                raise ValueError(f"Missing required entries in {section} section!")

        return config
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Using default configuration.")
        return {}  # or return default configuration dictionary
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        return {}  # or handle exception as appropriate
    
    
    
def store_solution(oil_distribution_history, filename):
    """
    Stores the oil distribution history to a file.

    Parameters:
    oil_distribution_history (list): List of dictionaries or arrays representing oil distribution at each time step.
    filename (str): Path to the file to store the solution.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(oil_distribution_history, file, indent=4)
        print(f"Saved solution to {filename}.")
        
    except Exception as e:
        print(f"Error saving solution to {filename}: {e}")
              
      
              
def load_solution(filename, start_time = None):
    """
    Loads the oil distribution history from a file.

    Parameters:
    filename (str): Path to the file containing the solution.
    t_restart (int or None): Restart time step. If provided, starts simulation from this time step.

    Returns:
    list: List of dictionaries or arrays representing oil distribution at each time step.
    """
    try:
        with open(filename, 'r') as file:
            oil_distribution_history = json.load(file)
            
        # If start_time is provided, find the closest time step in the history:
        if start_time is not None:
            closest_time_step = min(oil_distribution_history.keys(), key=lambda x: abs(x - start_time))
            print (f"Restart the simulation from time step {closest_time_step}.")
            
        return oil_distribution_history
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except json.JSONDecodeError as je:
        print(f"Error decoding JSON from {filename}: {je}")
        return None
    except Exception as e:
        print(f"Error loading solution from {filename}: {e}")
        return None
            