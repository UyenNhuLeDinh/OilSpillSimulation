import math
import numpy as np
from abc import ABC, abstractmethod


class CellFactory:
    """Create cell instances based on a cell type.
    """
    def __init__(self) -> None:
        """Initialize the CellFactory with an empty list for registering cells
        """
        self._cellTypes = {}

    # Register cell types with a specific key:
    def register(self, key, name):
        """Register a cell type with a specific key showing the cell type
    
        Parameters: 
        - key (str): The key showing the cell type. 
        - cell_type (type): The class of the cell type. 
        """
        self._cellTypes[key] = name

    # Make the instance of the CellFactory callable: looks up the coresponding
    # cell type in the cellTypes dictionary and create a new cell object
    def __call__(self, key, pts, idx, coord):
        """Create a new cell object based on the registered cell type.

        Parameters:
        - pts : The points' indices.
        - idx : The index of the cell.
        - coord : The coordinates of the points in the cell.

        Returns:
        - An instance of the cell type.
        """
        return self._cellTypes[key](pts, idx, coord)


class Cell(ABC):
    def __init__(self, pts, idx, coord) -> None:
        """
        Abstract cell class.

        Initialize a cell with given points, index of a cell, and coordinates of each point. 

        Parameters: 
        - pts (list[int])     : point ids of cell
        - idx (int)           : index of cell
        coord (list[array]) : coordinates of points

        Returns: 
        - None
        """
        self._pointIDs = pts
        self._idx = idx
        self._coord = coord

        # Variables
        self._oil_point = np.array([0.35, 0.45])
        self._neighbors_indices = []
        self._midpoint = self.computeMidpoint()
        self._velocity = self.computeVelocity()
        self._oil = self.computeOil()

    def computeNeighbor(self, all_cells):
        """
        Compute the neighbors of the cell.  

        Parameters: 
        - all_cells (list[Cell]): List of all cell instances. 

        Returns: 
        - list[int]: List of indexes of neighboring cells of the current cell. 
        """
        for cell in all_cells:
            if cell._idx != self._idx:
                if isinstance(cell, Triangle) or isinstance(cell, Line):
                    common_points = set(cell._pointIDs) & set(self._pointIDs)
                    if len(common_points) == 2:
                        self._neighbors_indices.append(cell._idx)
        return self._neighbors_indices

    @abstractmethod
    def computeMidpoint(self):
        """
        Compute the midpoint of each cell. 
        
        Returns: 
        - np.array: The coordinates of the midpoint. 
        """
        pass

    def computeVelocity(self):
        """ 
        Compute the velocity at the midpoint of each cell. 

        Returns: 
        - np.array: The velocity of the cell.  
        """
        midpoint = np.array(self._midpoint)
        # Velocity at midpoint in x-direction:
        v_x = midpoint[1] - 0.2 * midpoint[0]
        # Velocity at midpoint in y-direction:
        v_y = -midpoint[0]
        return np.array([v_x, v_y])

    def computeOil(self):
        """ 
        Compute the amount of oil in each cell. 

        Returns: 
        - float: The computed amount of oil. 
        """
        squared_distance = np.sum(np.square(self._midpoint - self._oil_point))
        u = math.exp(- squared_distance / 0.01)
        return u


class Triangle(Cell):
    """ Create a subclass Triangle of a class Cell. 
    
    The Triangle class is a child class of the Cell class. 
    """
    def __init__(self, pts, idx, coord) -> None:
        """ 
        Initialize a Triangle cell. 

        Parameters: 
        - pts (list[int]): Point IDs of the cell. 
        - idx (int): Index of the  cell. 
        - coord (list[array]): Coordinates of the vertexes in the triangle. 

        Returns:
        - None 
        """
        super().__init__(pts, idx, coord)
        self._neighbors_indices = []
        self._area = self.computeArea()
        
    def __str__(self):
        """ 
        String representation of the Triangle cell printing out its neighbors. 

        Returns: 
        - str: A string describing the cell and neighbors of the cell. 
        """
        return f"Triangle{self._idx} has neighbors with indices: {[neighbors for neighbors in self._neighbors_indices]}"

    def computeMidpoint(self):
        """ 
        Compute the midpoint of the Triangle Cell. 

        Returns: 
        - np.array: The coordinates of the midpoint. 

        Raises: 
        - ValueError: If the number of coordinates are not three. 
        """
        if len(self._coord) != 3:
            raise ValueError("Triangle cells must have exactly 3 coordinates.")
        coords = np.array(self._coord)[:, :2]
        midpoint = np.mean(coords, axis=0)
        return midpoint
    
    def computeArea(self):
        """ 
        Compute the area of each cell. 

        Returns: 
        - float: The area of the triangle. 
        """
        p1 = self._coord[0]
        p2 = self._coord[1]
        p3 = self._coord[2]
        A = 0.5 * abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])))
        return A



class Line(Cell):
    """
    Create a subclass Triangle of a class Cell. 

    The Triangle class is a child class of the Cell class.
    """ 
    def __init__(self, pts, idx, coord) -> None:
        """ 
        Initialize a Line cell.

        Parameters: 
        - pts (list[int]): Point IDs of the cell. 
        - idx (int): Index of the  cell. 
        - coord (list[array]): Coordinates of the vertexes in the triangle. 

        Returns:
        - None 
        """
        super().__init__(pts, idx, coord)
        self._neighbors_indices = []
        
    def __str__(self):
        """ 
        String representation of the Line cell printing out its neighbors. 

        Returns: 
        - str: A string describing the cell and neighbors of the cell. 
        """
        return f"Line{self._idx} has neighbors with indices: {[neighbors for neighbors in self._neighbors_indices]}"

    def computeMidpoint(self):
        """ 
        Compute the midpoint of the Line Cell. 

        Returns: 
        - np.array: The coordinates of the midpoint. 

        Raises: 
        - ValueError: If the number of coordinates are not two. 
        """
        if len(self._coord) != 2:
            raise ValueError("Line cells must have exactly 2 coordinates.")
        coords = np.array(self._coord)[:, :2]
        midpoint = np.mean(coords, axis=0)
        return midpoint
