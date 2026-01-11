import numpy as np
import time
from chaos4.integrators import Solver
from chaos4.viz import Visualizer

def bounded_snap(x, v, a, j, t):
    A, B, C, D, E = 0.6, 1.5, 1.5, 0.5, 4.0
    return -A*j - B*a - C*v - D*x + E*np.tanh(x)

def run_stress_test():
    solver = Solver(bounded_snap)
    
    # 1. High-Load Performance Test
    print("STRESS TEST: High-Load Simulation (1,000,000 steps)...")
    y0 = [0.1, 0.0, 0.0, 0.0]
    t_span = (0, 1000)
    dt = 0.001
    
    start_time = time.time()
    t, states = solver.solve(y0, t_span, dt, method='rk4')
    end_time = time.time()
    
    print(f"Completed 1M steps in {end_time - start_time:.4f} seconds.")
    print(f"Final state: {states[-1]}")
    
    # 2. Sensitivity Test (Butterfly Effect)
    print("\nSTRESS TEST: Sensitivity Analysis (Initial Perturbation 1e-10)...")
    y1 = [0.1, 0.0, 0.0, 0.0]
    y2 = [0.1 + 1e-10, 0.0, 0.0, 0.0]
    
    t_short = (0, 200)
    _, states1 = solver.solve(y1, t_short, dt)
    _, states2 = solver.solve(y2, t_short, dt)
    
    divergence = np.linalg.norm(states1 - states2, axis=1)
    print(f"Initial divergence: {divergence[0]:.2e}")
    print(f"Final divergence: {divergence[-1]:.2e}")
    
    if divergence[-1] > divergence[0] * 1e5:
        print("RESULT: Exponential divergence confirmed. System is chaotic.")
    else:
        print("RESULT: Low divergence. System may be periodic or stable.")

    # 3. Symplectic Integrator Check
    print("\nSTRESS TEST: Symplectic Integrator Stability...")
    try:
        _, states_sym = solver.solve(y0, (0, 100), dt, method='symplectic')
        print(f"Symplectic final state: {states_sym[-1]}")
        print("RESULT: Symplectic engine operational.")
    except Exception as e:
        print(f"RESULT: Symplectic engine failure: {e}")

if __name__ == "__main__":
    run_stress_test()
