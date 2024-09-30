import meshio
from .cells import CellFactory, Line, Triangle


class Mesh:
    """ 
    Manages a mesh structure by creating instances of different cell types
    """
    def __init__(self, mshName) -> None:
        """ 
        Initialize the Mesh by reading the mesh file and setting up cell instances. 

        Parameters: 
        - mshName(str): The mesh file to be read. 

        Returns: 
        - None 
        """
        # Read in the mesh file:
        msh = meshio.read(mshName)

        # Extract the points and cells from the mesh:
        cells = msh.cells
        self._points = msh.points   # List of points' coordinates

        # Initialize the list to store all cells instances:
        self._cells_instances = []

        # Initialize the CellFactory and register cell types:
        cf = CellFactory()
        cf.register("line", Line)
        cf.register("triangle", Triangle)

        idx = 0
        for cellForType in cells:
            cellType = cellForType.type
            if cellType not in cf._cellTypes:
                continue
            cellPoints = cellForType.data
            # Iterate over each set of points to create cell instances:
            for pts in cellPoints:
                # Extract coordinates of points using their indices:
                coord = [self._points[index] for index in pts]
                # Create a cell instance using the factory and append it to
                # the cell instance list:
                self._cells_instances.append(cf(cellType, pts, idx, coord))
                idx += 1

    def computeallneighbors(self):
        """
        Compute neighbors for all cells. 
        
        Returns:
        - None 
        """
        for cell in self._cells_instances:
            # Compute neighbors for each cell
            cell.computeNeighbor(self._cells_instances)