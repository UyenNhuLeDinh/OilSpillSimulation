# Project Title: SIMULATION OF OIL SPILL
Course INF203 - Advanced Programming Project
Task: MODELING OIL SPILL DYNAMICS: A COMPUTATIONAL APPROACH
Authors
MIN JEONG CHEON
LE UYEN NHU DINH


# Description
Create a robust simulation model capable of accurately predicting the oil distribution over time on the Bay City's coastal area.

### Modules

The package is split into 7 modules:

1. mesh.py
2. cells.py
3. simulation.py
4. visualization.py
5. io_operations.py
6. logger.py
7. main.py

### Tests

The package has tests split into 3 files
1. test_cells.py
2. test_mesh.py
3. test_simulation.py

### Configuration files

The package has 4 input settings (configuration files)
1. input.toml (#default)
2. config1.toml
3. config2.toml
4. config3.toml


# Running the Simulation
To execute the simulation and utilize its features, run the main.py script with appropriate command-line arguments. Below are the available options:

## Command-line Arguments:
-c, --config: Specifies the path to the configuration file. Default: configs/input.toml
--store-solution: Option to store the solution as a text file.
--plot: Option to plot the final oil distribution.
--video: Option to create an oil distribution video.
--log-summary: Option to log simulation summary.
--startTime: Specifies the time to resume simulation from the restart file.

## Example Usage:
Running the command line below produces a plot showing the final oil distribution over time and a video illustrating oil spread:
python main.py -c configs/input.toml --plot --store-solution --video

## Accessing Results:
Navigate to the following folders within the project directory:

Group37DinhCheon/
├── configs/
│   ├── input.toml
│   ├── config1.toml
│   ├── config2.toml
│   ├── config3.toml
├── results/
│   ├── input_results/
│   │   ├── final_plot.png
│   │   ├── OilFishingSummary
│   │   ├── simulation_video.mp4
│   │   └── solution.json
│   ├── config1_results/
│   │   └── ...
│   ├── config2_results/
│   │   └── ...
│   ├── config3_results/
│   │   └── ...
├── main.py
└── ...

## Through provided command lines for main.py, users can obtain:

    - Final Oil Distribution Plots: Visual representations stored as final_plot.png for detailed analysis.
    - Text Files: solution.json files containing detailed records of oil amounts per cell at each time step.
    - Simulation Videos: simulation_video.mp4 illustrating the progression of oil spread over time.
    - Logger: OilFishingSummary file logging the amount of oil in the fishing grounds over time.
    - Start simulation from a starting time (only if args.startTime is given) from a solution text file (input "restartFile" from configuration file)
    




