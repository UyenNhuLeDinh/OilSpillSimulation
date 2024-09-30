import argparse
import os
import logging
import matplotlib.pyplot as plt
from src.Simulation.mesh import Mesh
from src.Simulation.cells import *
from src.Simulation.simulation import Simulation
from src.Simulation.visualization import plotting, video
from src.Simulation.io_operations import read_config_file, store_solution, load_solution
from src.Simulation.logger import log_summary
def parse_arguments():
    """
    Parse command line arguments.

    Returns: 
    - args: Parsed command line arguments. 
    """
    
    parser = argparse.ArgumentParser(description='Oil Spill Simulation and Visualization')
    parser.add_argument('-c', '--config', type=str, default='configs/input.toml', help='Path to the configuration file (default: configs/input.toml)')
    parser.add_argument("--store-solution", action="store_true", help="Store the solution as a text file")
    parser.add_argument("--plot", action="store_true", help="Plot the final oil distribution")
    parser.add_argument('--video', action='store_true', help='Create an oil distribution video')
    parser.add_argument("--log-summary", action="store_true", help="Log simulation summary")
    parser.add_argument('--startTime', type=int, help='Time to start the simulation from the restart file')
    args = parser.parse_args()
    
    print(f"Config file: {args.config}")
    print(f"Start time: {args.startTime}")
    return args

def create_results_dir(config_path):
    """ 
    Create a path and directory for saving the simulation results. 

    Parameters: 
    - config_path (str): Path to the configuration file. 

    Returns: 
    - results_dir (str): Path to the created results directory.  
    """
    config_name = os.path.splitext(os.path.basename(config_path))[0]
    results_dir = os.path.join('results', f'{config_name}_results')
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

if __name__ == "__main__":
    """ 
    Main script to run the simulation 

    The script initializes the mesh and simulation, runs the simulation, stores the 
    solution, plot the final oil distribution, create a video of the simulation, and logs a summary. 
    """
    # Step 1: Parse command line arguments
    args = parse_arguments()
    
    # Step 2: Read the configuration file
    config_file = args.config 
    if not os.path.isfile(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        exit(1)
        
    config = read_config_file(config_file)
    if not config:
        print(f"Error: Configuration file '{config_file}' is empty or invalid.")
        exit(1)
    print(config)   # Debug print
    
    # Step 3: Extract simulation parameters
    try:
        mesh_path = config['Settings']['mesh_path']
        tStart = config['Settings']['tStart']
        tEnd = config['Settings']['tEnd']
        num_steps = config['Settings']['num_steps']

        x_range = config['FishingGround']['x_range']
        y_range = config['FishingGround']['y_range']

        logName = config['IO']['logName']
        write_frequency = config['IO']['writeFrequency']
        restartFile = config['IO'].get('restartFile', None)
    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
        exit(1)
        
    # Step : Create results directory
    results_dir = create_results_dir(args.config)
    
    # Step 4: Set up logging
    logging.basicConfig(filename=os.path.join(results_dir, logName), level=logging.INFO)

    
    # Step 5: Check if we have to restart from a text file:
    if restartFile and os.path.isfile(restartFile):
        oil_distribution_history = load_solution(restartFile, args.startTime)
    else:
        oil_distribution_history = []
        
    # Step 6: Initialize mesh
    mesh = Mesh(mesh_path)
    
    # Step 7: Initialize simulation
    sim = Simulation(mesh, tStart, tEnd, num_steps)
    if oil_distribution_history:
        sim.oil_distribution_history = oil_distribution_history
    else:
        sim.solution()

    
    # Step 8: Store the solution as a text file
    if args.store_solution:
        if write_frequency: 
            store_solution(sim.oil_distribution_history, os.path.join(results_dir, 'solution.json'))
    
    # Step 9: Plot the final oil distribution
    if args.plot:
        # Generate final plot
        final_fig, final_ax = plotting(mesh, sim.oil_distribution_history[-1], 'final_plot.png', tEnd)
        plt.savefig(os.path.join(results_dir, 'final_plot.png'))
        plt.close(final_fig)
    
    # Step 10: Create video if writeFrequency is given:
    if args.video:
        video(mesh, sim.oil_distribution_history, 
                               os.path.join(results_dir, 'simulation_video.mp4'), write_frequency)
                
    # Step 8: Log simulation summary 
    if args.log_summary:
        log_summary(config_file, sim.oil_distribution_history)
        
