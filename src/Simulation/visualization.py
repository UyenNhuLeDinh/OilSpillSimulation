import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import cv2 # type: ignore
import os
from .cells import *
from .mesh import Mesh
from .simulation import Simulation

def draw_mesh(mesh, ax):
    """ 
    Draw mesh based on the given axis. 

    Parameters: 
    - mesh (Mesh): The mesh file with cells and points information. 
    - ax (matplotlib.axes.Axes): The axis on which to draw the mesh. 
    """
    for cell in mesh._cells_instances:
        if isinstance(cell, Triangle):
            p1, p2, p3 = [mesh._points[pid][:2] for pid in cell._pointIDs]
            ax.plot([p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], color='#8A2BE2', linewidth=1, zorder=1, alpha=0.5)


def plotting(mesh, oil_distribution, figname, time, title = "Oil Distribution"):
    """
    Plot the oil distribution on the mesh grid.

    Parameters:
    - mesh: Mesh object containing cells and points.
    - oil_distribution: List mapping cell indices to oil amount.
    - figname (str): File name to save the plot.
    - time (float): Time to show in the title of the plot. 
    - title (str): Title of the plot.
    """
    fig, ax = plt.subplots()
    draw_mesh(mesh, ax)
    
    # Define a colormap and normalization
    norm = Normalize(vmin=min(oil_distribution.values()), vmax=max(oil_distribution.values()))
    cmap = plt.cm.viridis
    cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1]) 
        
    # Plot each cell with heatmap colors
    for cell in mesh._cells_instances:
        if isinstance(cell, Triangle):
            p1, p2, p3 = [mesh._points[pid][:2] for pid in cell._pointIDs]
            face_color = cmap(norm(oil_distribution[cell._idx]))
            triangle = plt.Polygon([p1, p2, p3], edgecolor='none', facecolor=face_color, zorder=2)
            ax.add_patch(triangle)
            
    # Create a colorbar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Amount of oil')
    
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f"{title}\n at t = {time:.2f}")
    
    return fig, ax
    

def video(mesh, oil_distribution_history, video_name, fps):
    """
    Create a video showing changes in plots of oil distribution over time.

    Parameters:
        mesh (Mesh): The mesh object.
        oil_distribution_history (list): List of oil distribution data at different time steps.
        video_name (str): Name of the output video file.
        fps (int): Frames per second for the output video.
    """
    
    # List to store plot image filenames
    plot_images = []
    
    # Loop through frames
    for i, oil_distribution in enumerate(oil_distribution_history):
        if i % 10 == 0:
            
            # Plot oil distribution for current frame
            fig, ax = plotting(mesh, oil_distribution, 'plot',time =i, title='Oil Distribution')
        
            # Save plot as image file
            plot_image_file = f"plot_{i}.png"
            fig.savefig(plot_image_file)
            plt.close(fig)
        
            plot_images.append(plot_image_file)
    
    # Read the dimensions of the first image
    height, width, _ = cv2.imread(plot_images[0]).shape
    
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
    
    # Write images to video
    for plot_image_file in plot_images:
        frame = cv2.imread(plot_image_file)
        video_writer.write(frame)
        os.remove(plot_image_file)  # Remove the temporary image file
        
    video_writer.release()


if __name__ == '__main__':
    """ 
    A script to simulate the oil spill and make plots. 
    """
    mesh = Mesh('src/Simulation/bay.msh')
    tStart = 0.0
    tEnd = 0.6
    num_steps = 100
    sim = Simulation(mesh, tStart, tEnd, num_steps)
    sim.solution()
    
    # Plot after every 0.1 time unit
    time_interval = 0.1
    for i in range(num_steps):
        time = tStart + i * (tEnd - tStart) / num_steps
        if time % time_interval == 0:
            figname = f"oil_distribution_{time:.1f}.png"  # Adjust the filename as needed
            plotting(mesh, sim.oil_distribution_history[i], figname, time)