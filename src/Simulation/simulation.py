from src.Simulation.mesh import *
from src.Simulation.cells import *
import numpy as np # type: ignoreimport math


class Simulation:
    """ 
    Runs oil spill simulation for certain time interval on a given mesh file. 
    """
    
    def __init__(self, mesh, tStart, tEnd, num_steps) -> None:
        """ 
        Initialize the simulation. 
        
        Parameters: 
        - mesh(Mesh): The mesh about cells and points. 
        - tStart(float): The start time of the simulation. 
        - tEnd (float): The end time of the simulation.
        - num_steps (int): The number of time steps that the simulation would run.  
        
        Returns:
        - None 
        """
        self._mesh = mesh
        self._tStart = tStart
        self._tEnd = tEnd
        self._num_steps = num_steps
        
        self._dt = (tEnd - tStart) / num_steps
        self.oil_distribution = {cell._idx: cell._oil for cell in mesh._cells_instances}
        self.oil_distribution_history = []
        
        
    def computeAverageVelocity(self, cell, neighbor_index):
        """ 
        Compute the average velocity between the current cell and its neighbors cell. 

        Parameters: 
        - cell (Cell): The current cell. 
        - neighbor_index (int): The index of the neighboring cell. 

        Returns: 
        - np.array: The average velocity. 
        
        """
        neighbor_cell = self._mesh._cells_instances[neighbor_index]
        # Find the velocity in the current cell
        v_i = cell._velocity
        # Find the velocity in the neighbor cell
        v_n = neighbor_cell._velocity
        # Compute the average velocity
        a_v = (v_i + v_n) / 2
        return a_v
    
       
    def computeScaleNormal(self, cell, neighbor_index):
        """ 
        Compute the scaled normal for the edge that is shared by the current cell and its neighbor based on given formula. 

        Parameters: 
        - cell (Cell): The current cell. 
        - neighbor_index (int): The index of the neighboring cell. 

        Returns: 
        - np.array: The scaled normal vector. 
        """
        neighbor_cell = self._mesh._cells_instances[neighbor_index]
        common_point = set(cell._pointIDs) & set(neighbor_cell._pointIDs)

        if len(common_point) == 2:
            shared_edge = list(common_point)
            x1, y1 = self._mesh._points[shared_edge[0]][:-1]
            x2, y2 = self._mesh._points[shared_edge[1]][:-1]

            edge_vector = np.array([x2 - x1, y2 - y1])
            normal_vector = np.array([edge_vector[1], -edge_vector[0]])
            unit_normal = normal_vector / np.linalg.norm(normal_vector)
            
            # Check the orientation:
            midpoint_of_cell = cell._midpoint
            midpoint_of_edge = np.array([(x1 + x2) / 2, (y1 + y2) / 2]) - midpoint_of_cell
            if np.dot(unit_normal, midpoint_of_edge) < 0:
                unit_normal = -unit_normal
            scaled_normal = unit_normal * np.linalg.norm(edge_vector)
        return scaled_normal
    
    
    def solution(self):
        """ 
        Run the simulation to calculate the oil distribution, update it, and save it. 
        
        Returns:
        - None
        """
        self._mesh.computeallneighbors()
        self.oil_distribution_history.append(self.oil_distribution.copy())
        
        for _ in range(self._num_steps):
            new_oil_distribution = self.oil_distribution.copy()
            
            for cell in self._mesh._cells_instances:
                if isinstance (cell, Triangle):
                    total_flux = 0.0
                
                    for neighbor in cell._neighbors_indices:
                        # Look up average velocity:
                        v = self.computeAverageVelocity(cell, neighbor)
                        # Look up scaled normal:
                        n = self.computeScaleNormal(cell, neighbor)
                    
                        dot_product = np.dot(v, n)
                        if dot_product > 0:
                            g = new_oil_distribution[cell._idx] * dot_product
                        else:
                            g = new_oil_distribution[neighbor] * dot_product
                    
                        F = -(self._dt / cell._area) * g
                        total_flux += F
                    
                    # Update the copied oil distribution
                    new_oil_distribution[cell._idx] += total_flux
            
            # Update the oil distribution for the next step:
            self.oil_distribution = new_oil_distribution
            
            # Append the updated oil distribution to history
            self.oil_distribution_history.append(new_oil_distribution.copy())
