import pytest
import numpy as np
import math
from src.Simulation.mesh import Mesh
from src.Simulation.cells import Cell, Line, Triangle, CellFactory

@pytest.fixture
def testmesh():
    """ 
    Fixture to create a Mesh for testing. 

    Returns: 
    - Mesh: A Mesh created for testing. 
    """
    mesh_path = 'tests/simple_mesh.msh'
    return Mesh(mesh_path)


def test_CellFactory(testmesh):
    """ 
    Test the CellFactory. 
    - Checks if each cell type is registered in the CellFactory.
    - Checks if the created cell instance matches the attributes of the original cell.
    """

    # Initialize the CellFactory:
    cf = CellFactory()
    
    # Register the cell types:
    cf.register('line', Line)
    cf.register('triangle', Triangle)
    
    # Check if each cell is created and registered correctly:
    for cell in testmesh._cells_instances:
        cell_type = cell.__class__.__name__.lower()
        assert cell_type in cf._cellTypes
        
        # Save the information:
        pts = cell._pointIDs
        idx = cell._idx
        coord = cell._coord

        # Create cell instance using CellFactory:
        created_cell = cf(cell_type, pts, idx, coord)
        
        # Verify the created cell instance attributes:
        assert isinstance(created_cell, cell.__class__)
        assert np.array_equal(created_cell._pointIDs, pts)
        assert np.array_equal(created_cell._idx, idx)
        assert np.array_equal(created_cell._coord, coord)
        
        
def test_computeNeighbor(testmesh):
    """ 
    Test the computeNeighbor method in the Cell class. 
    - Checks if each cell ahs the computeNeighbor method. 
    - Checks if the computed neighbor indices are correct. 
    - Checks if the neighbor is actually in the cell instances    
    """
    # Run the function computeallneigbors in Class Mesh:
    testmesh.computeallneighbors()
    
    # Check if each cell instance is able to call the computing function:
    for cell in testmesh._cells_instances:
        assert hasattr(cell, 'computeNeighbor'), f" Cell {cell._idx} does not have the computeNeighbor method."
        
        # Check if the computed neighboring indices are correct:
        for neighbor_index in cell._neighbors_indices:
            assert neighbor_index != cell._idx, f"Cell {cell._idx} contains itself in the neighbor indices list."
            
            # Check if the index of the neighbor is actually in the cell instances list from the mesh:
            neighbor_found = False
            for neighbor in testmesh._cells_instances:
                if neighbor._idx == neighbor_index:
                    neighbor_found = True
                    break
                
            assert neighbor_found, f" Cell {cell._idx} has invalid neighbor index {neighbor_index}"
            
    
def test_computeMidpoint(testmesh):
    """ 
    Test the computeMidpoint method in the Cell class. 
    - Checks if computed midpoint is close to the expected midpoint
    """
    # Run the tested function:
    for cell in testmesh._cells_instances:
        midpoint = cell.computeMidpoint()
        
        # Manually compute the midpoint coordinates for the cell and remove the z-coordinate (2D mesh):
        expected_midpoint = np.mean([testmesh._points[pt_idx] for pt_idx in cell._pointIDs], axis=0)[:-1]
        
        # Assert that the computed midpoint is close to the expected midpoint
        assert np.allclose(midpoint, expected_midpoint), f"Cell {cell._idx} got unmatched midpoint's coordinates."

            
def test_computeVelocity(testmesh):
    """ 
    Test the computeVelocity method in the Cell class. 
    - Checks if the computed velocity is in 2D and stored in a tuple 
    - Checks if the accuracy on each component of the velocity 
    """
    # Run the tested function:
    for cell in testmesh._cells_instances:
        velocity = cell.computeVelocity()
        
        # Check if the computed velocity is in 2D and stored in a tuple:
        assert len(velocity) == 2 , f" Cell {cell._idx} has unmatched form of velocity with the requirement."
        assert isinstance(velocity, np.ndarray), "Velocity should be stored in a NumPy array"
        
        # Assert the values of velocity components based on the formula provided:
        midpoint = cell._midpoint
        expected_v_x = midpoint[1] - 0.2 * midpoint[0]
        expected_v_y = - midpoint[0]
        
        # Check the accuracy on each component of the velocity:
        assert np.isclose(velocity[0], expected_v_x), f"Velocity component v_x is incorrect: {velocity[0]}"
        assert np.isclose(velocity[1], expected_v_y), f"Velocity component v_y is incorrect: {velocity[1]}"
        

def test_computeOil(testmesh):
    """ 
    Test the computeOil method in the Cell class. 
    - Checks if the computed oil amount is close to the expected amount of oil value. 
    """
    # Run the tested function:
    for cell in testmesh._cells_instances:
        u = cell.computeOil()
        
        # Manually compute the oil:
        expected_distance = np.sum(np.square(cell._midpoint - cell._oil_point))
        expected_u = math.exp(- expected_distance / 0.01)
        
        # Checks if the computed amount of oil is correct 
        assert np.isclose(u, expected_u) , f" Cell {cell._idx} has incorrect computed the initial amount of oil."
        
        
def test_computeArea(testmesh):
    """
    Test the computeArea method in the Cell class.
    - Checks if the area value for each type of cells is correct. 
    """
    # Run the tested function:
    for cell in testmesh._cells_instances:
        # Check the area value for each type of cells:
        if isinstance(cell, Triangle):
            A = cell.computeArea()
            vector1 = testmesh._points[cell._pointIDs[1]] - testmesh._points[cell._pointIDs[0]]
            vector2 = testmesh._points[cell._pointIDs[2]] - testmesh._points[cell._pointIDs[0]]
            expected_area = 0.5 * np.linalg.norm(np.cross(vector1, vector2))
            assert np.isclose(A, expected_area), f"Triangle cell {cell._idx} has incorrect value of area."