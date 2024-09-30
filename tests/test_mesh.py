import pytest
import numpy as np
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


def test_mesh_initialization(testmesh):
    """ 
    Test the initialization in the Mesh class. 
    - Checks if the mesh points match the expected values. 
    - Checks if the cell instances are created correctly. 
    """
    # Verify mesh points:
    expected_points = np.array([[0, 1, 0], [1, 1, 0], [1, -0, 0], [0, -0, 0], [0.5, 0.5, 0]]) 
    assert np.array_equal(testmesh._points, expected_points)

    # Check if the cell instances are created correctly: there are 4 line elements and 4 triangle elements
    assert len(testmesh._cells_instances) == 8
    
    
def test_compute_neighbors(testmesh):
    """ 
    Test the compute_neighbors method in the Mesh class. 
    - Checks if the function computeNeighbor from class Cell is called for each instance.
    """ 
    # Run the function needed to be tested:
    testmesh.computeallneighbors()
    
    # Verify that the function computeNeighbor from class Cell is called for each instance:
    for cell in testmesh._cells_instances:
        expected_neighbors_indices = cell._neighbors_indices
        assert sorted(cell._neighbors_indices) == sorted(expected_neighbors_indices)

