import pytest
import numpy as np
from src.Simulation.mesh import Mesh
from src.Simulation.cells import Cell, Line, Triangle, CellFactory
from src.Simulation.simulation import Simulation

@pytest.fixture
def testmesh():
    """ 
    Fixture to create a Mesh for testing. 

    Returns: 
    - Mesh: A Mesh created for testing. 
    """
    mesh_path = 'tests/simple_mesh.msh'
    return Mesh(mesh_path)

def test_simulation_initialization(testmesh):
    """ 
    Test the initialization of Simulation class.
    - Checks if the attributes in the Simulation instance match the expected values. 
    - Checks if the oil distribution is initialized correctly. 
    - Checks if the oil distribution history is initially an empty list. 
    """
    tStart = 0
    tEnd = 0.5
    num_steps = 500
    sim = Simulation(testmesh, tStart, tEnd, num_steps)

    assert sim._mesh == testmesh
    assert sim._tStart == tStart
    assert sim._tEnd == tEnd
    assert sim._num_steps == num_steps
    assert sim._dt == (tEnd - tStart) / num_steps

    # Check oil distribution initialization
    for cell in sim._mesh._cells_instances:
        if isinstance (cell, Triangle):
            expected_oil = cell._oil 
            assert sim.oil_distribution[cell._idx] == expected_oil

        assert sim.oil_distribution_history == []


def test_computeAverageVelocity(testmesh):
    """ 
    Test the computeAverageVelocity method in the Simulation class.
    - Checks if the the velocity in the current cell matches the expected value. 
    """
    sim = Simulation(testmesh, 0, 0.5, 500)
    for cell in sim._mesh._cells_instances: 
        if isinstance(cell, Triangle) or isinstance(cell, Line):
            for neighbor_index in cell._neighbors_indices: 
                neighbor_cell = sim._mesh._cells_instances[neighbor_index]
                # Find the velocity in the current cell
                v_ix, v_iy = cell._velocity
                # Find the velocity in the neighbor cell
                v_nx, v_ny = neighbor_cell._velocity
                a_v = np.array([(v_ix + v_nx) / 2, (v_iy + v_ny) / 2])
                expected = sim.computeAverageVelocity(cell, neighbor_index)
                assert np.allclose(a_v, expected)

def test_computeScaleNormal(testmesh):
    """ 
    Test the computeScaleNormal method in the Simulation class.
    - Checks if the computed normal matches the expected result. 
    """
    sim = Simulation(testmesh, 0, 0.5, 500)
    
    for cell in sim._mesh._cells_instances:
        if isinstance(cell, Triangle) or isinstance(cell, Line):
            for neighbor_index in cell._neighbors_indices:
                neighbor_cell = sim._mesh._cells_instances[neighbor_index]
                common_points = set(cell._pointIDs) & set(neighbor_cell._pointIDs)
                
                if len(common_points) == 2:
                    shared_edge = list(common_points)
                    x1, y1 = sim._mesh._points[shared_edge[0]][:-1]
                    x2, y2 = sim._mesh._points[shared_edge[1]][:-1]

                    # Calculate the edge vector
                    edge_vector = np.array([x2 - x1, y2 - y1])
                    length_edge = np.linalg.norm(edge_vector)
                    
                    # Compute the normal vector to the edge
                    normal_vector = np.array([edge_vector[1], -edge_vector[0]])
                    length_normal = np.linalg.norm(normal_vector)
                    unit_normal = normal_vector / length_normal
                    
                    # Get the midpoint of the current cell
                    midpoint_of_cell = np.array(cell._midpoint)
                    
                    # Calculate the midpoint of the shared edge
                    midpoint_of_edge = np.array([(x1 + x2) / 2, (y1 + y2) / 2]) - midpoint_of_cell
                    
                    # Ensure the normal vector points outward from the cell
                    if np.dot(unit_normal, midpoint_of_edge) < 0:
                        unit_normal = -unit_normal
                    
                    # Scale the normal vector by the length of the edge
                    scaled_normal = unit_normal * length_edge
                    
                    # Compute the expected scaled normal using the method
                    expected = sim.computeScaleNormal(cell, neighbor_index)
                    
                    # Assert the computed normal matches the expected result
                    assert np.allclose(scaled_normal, expected), f"Failed for cell {cell} and neighbor {neighbor_index}"
                    
                    

def test_solution_function(testmesh):
    """ 
    Test the solution_function method in the Simulation class.
    - Checks if the oil distribution for the current cell is updated. 
    - Check if the number of keys in oil_distribution_history is same as num_steps. 
    """
    # Initialize the simulation
    sim = Simulation(testmesh, 0, 0.5, 50)
    sim._mesh.computeallneighbors()

    # Run the solution method
    sim.solution()

    # Check each triangle cell's oil update
    for cell in sim._mesh._cells_instances:
        if isinstance(cell, Triangle):
            # Check if the oil distribution for the current cell is updated
            assert cell._idx in sim.oil_distribution_history[-1], f"Oil distribution not updated for cell {cell._idx}"

    # Check if the number of keys in oil_distribution_history is same as num_steps
    assert len(sim.oil_distribution_history) == sim._num_steps + 1, "Mismatch in number of time steps"
