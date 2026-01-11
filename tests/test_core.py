import numpy as np
import pytest
from chaos4.integrators import Solver

def linear_snap(x, v, a, j, t):
    # Simple linear oscillator for baseline verification
    return -x

def test_solver_initialization():
    """Verify that the Solver accepts the mathematical operator."""
    solver = Solver(linear_snap)
    assert solver.snap_func == linear_snap

def test_state_space_reduction():
    """Verify the conversion from 4th-order scalar to 1st-order vector."""
    solver = Solver(linear_snap)
    y = np.array([1.0, 0.5, 0.2, 0.1])
    dy = solver._state_derivative(y, 0)
    
    # Expected: [v, a, j, f(x,v,a,j,t)]
    expected = np.array([0.5, 0.2, 0.1, -1.0])
    assert np.allclose(dy, expected)

def test_rk4_progression():
    """Verify temporal propagation via RK4."""
    solver = Solver(linear_snap)
    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    dt = 0.01
    y1 = solver.rk4_step(y0, 0, dt)
    
    # After one step, position should decrease slightly due to negative snap
    assert y1[0] < y0[0]
    assert len(y1) == 4

def test_integration_stability():
    """Verify long-term stability for a known linear system."""
    solver = Solver(linear_snap)
    y0 = [1.0, 0.0, 0.0, 0.0]
    t, states = solver.solve(y0, (0, 10), 0.1)
    
    assert states.shape == (100, 4)
    assert not np.any(np.isnan(states))
