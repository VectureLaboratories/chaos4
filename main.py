import numpy as np
from chaos4.integrators import Solver
from chaos4.viz import Visualizer

def quartic_snap_oscillator(x, v, a, j, t):
    """
    Operational Directive: Bounded Snap Equation.
    x^(4) = -A*j - B*a - C*v - D*x + E*tanh(x)
    Saturation is required to contain the attractor within the Vecture manifold.
    """
    A, B, C, D, E = 0.6, 1.5, 1.5, 0.5, 4.0
    return -A*j - B*a - C*v - D*x + E*np.tanh(x)

def main():
    # Calibrate Integration Engine
    solver = Solver(quartic_snap_oscillator)
    
    # Initial Conditions: [x, v, a, j]
    y0 = [0.1, 0.0, 0.0, 0.0]
    
    # Temporal Parameters
    t_span = (0, 500)
    dt = 0.01 
    
    print("Initiating simulation: Analyzing the Hidden Truth...")
    t, states = solver.solve(y0, t_span, dt, method='rk4')
    
    # Render Observable Manifold
    print("Projecting states onto 3D manifold...")
    Visualizer.plot_projection(states, indices=(0, 2, 3), labels=('x', 'Acceleration', 'Jerk'))
    
    # Extract Topological Invariants
    print("Generating Poincaré section: Locating islands...")
    ps_points = Visualizer.poincare_section(states, plane_idx=2, crossing_val=0)
    Visualizer.plot_poincare(ps_points, indices=(0, 1), labels=('x', 'Velocity'))

if __name__ == "__main__":
    main()