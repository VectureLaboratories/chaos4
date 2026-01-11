import numpy as np

class Solver:
    """
    Vecture-grade integration engine for 4th-order differential equations.
    
    This entity implements the State-Space Reducer to resolve Snap dynamics ($x^{(4)}$) 
    into actionable 1st-order vector fields. We provide multiple integration 
    schemes to ensure system integrity across varying manifolds.
    """

    def __init__(self, snap_func):
        """
        Calibrate the solver with the target snap function.

        Args:
            snap_func (callable): The mathematical operator f(x, v, a, j, t) 
                                 representing the 4th temporal derivative.
        """
        self.snap_func = snap_func

    def _state_derivative(self, y, t):
        """
        Internal mechanism for state-space dimensionality reduction.
        
        Args:
            y (np.ndarray): State vector [x, v, a, j].
            t (float): Temporal coordinate.

        Returns:
            np.ndarray: Time derivative of the state vector.
        """
        x1, x2, x3, x4 = y
        return np.array([
            x2,                                # Velocity
            x3,                                # Acceleration
            x4,                                # Jerk
            self.snap_func(x1, x2, x3, x4, t)  # Snap (Jounce)
        ])

    def rk4_step(self, y, t, dt):
        """
        Executes a single iteration of the 4th-order Runge-Kutta algorithm.
        
        Propagates the state vector through the temporal manifold with O(dt^4) precision.
        """
        k1 = self._state_derivative(y, t)
        k2 = self._state_derivative(y + k1 * dt / 2, t + dt / 2)
        k3 = self._state_derivative(y + k2 * dt / 2, t + dt / 2)
        k4 = self._state_derivative(y + k3 * dt, t + dt)
        return y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    def symplectic_step(self, y, t, dt):
        """
        Executes a single iteration of the 4th-order Forest-Ruth symplectic algorithm.
        
        Preserves the Hamiltonian structure for conservative systems. Essential 
        when energy dissipation is not permitted.
        """
        # Forest-Ruth calibration coefficients
        theta = 1.0 / (2.0 - 2.0**(1.0/3.0))
        
        # Sub-step 1: Initialization
        y = self._forest_ruth_substep(y, t, theta * dt / 2.0, theta * dt)
        # Sub-step 2: Mid-point Correction
        y = self._forest_ruth_substep(y, t + theta * dt, (1.0 - theta) * dt / 2.0, (1.0 - 2.0*theta) * dt)
        # Sub-step 3: Final Alignment
        y = self._forest_ruth_substep(y, t + (1.0-theta)*dt, (1.0 - theta) * dt / 2.0, theta * dt)
        # Sub-step 4: Termination
        y[0:3] += (theta * dt / 2.0) * y[1:4]
        
        return y

    def _forest_ruth_substep(self, y, t, dt_pos, dt_vel):
        """Internal operator for symplectic state updates."""
        # Update coordinates [x, v, a]
        y[0:3] += dt_pos * y[1:4]
        # Update momentum (Snap/Jerk relation)
        y[3] += dt_vel * self.snap_func(y[0], y[1], y[2], y[3], t)
        return y

    def solve(self, y0, t_span, dt, method='rk4'):
        """
        Integrates the system across the specified temporal horizon.

        Args:
            y0 (list or np.ndarray): Initial state vector [x, v, a, j].
            t_span (tuple): (t_start, t_end).
            dt (float): Integration step size.
            method (str): 'rk4' for dissipation or 'symplectic' for conservation.

        Returns:
            tuple: (time_array, state_history)
        """
        t_start, t_end = t_span
        t_values = np.arange(t_start, t_end, dt)
        n_steps = len(t_values)
        states = np.zeros((n_steps, 4))
        
        y = np.array(y0, dtype=float)
        step_func = self.rk4_step if method == 'rk4' else self.symplectic_step
        
        for i in range(n_steps):
            states[i] = y
            y = step_func(y, t_values[i], dt)
            
        return t_values, states