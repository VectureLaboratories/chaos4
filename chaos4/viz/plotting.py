import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Visualizer:
    """
    Observable manifold generator.
    
    This entity projects high-dimensional chaotic data into human-legible 
    manifolds while preserving the topological invariants of the 4D state space.
    """

    @staticmethod
    def plot_projection(states, indices=(0, 2, 3), labels=('x', 'a', 'j')):
        """
        Projects the 4D state vector onto a 3D observable manifold.

        Args:
            states (np.ndarray): Nx4 state matrix.
            indices (tuple): Indices for coordinate projection.
            labels (tuple): Axis nomenclature.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Rendering in Vecture Red (#ff3333)
        ax.plot(states[:, indices[0]], states[:, indices[1]], states[:, indices[2]], 
                lw=0.5, color='#ff3333') 
        
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
        ax.set_title("Vecture Chaos4 - Hyper-Chaotic Projection")
        plt.show()

    @staticmethod
    def poincare_section(states, plane_idx=2, crossing_val=0, direction=1):
        """
        Extracts the Poincaré section from the trajectory.
        
        Isolates crossings of the defined hyperplane to reveal the hierarchical 
        islands of stability within the hyper-chaotic flow.

        Args:
            states (np.ndarray): Nx4 state matrix.
            plane_idx (int): Coordinate index defining the hyperplane.
            crossing_val (float): Threshold for hyperplane intersection.
            direction (int): 1 for positive crossing, -1 for negative.

        Returns:
            np.ndarray: Intersection points on the manifold.
        """
        ps_points = []
        for i in range(len(states) - 1):
            s1 = states[i]
            s2 = states[i+1]
            
            # Intersection detection
            if (s1[plane_idx] - crossing_val) * (s2[plane_idx] - crossing_val) < 0:
                # Vector alignment check
                if direction * (s2[plane_idx] - s1[plane_idx]) > 0:
                    # Linear interpolation for sub-step precision
                    t = (crossing_val - s1[plane_idx]) / (s2[plane_idx] - s1[plane_idx])
                    point = s1 + t * (s2 - s1)
                    ps_points.append(point)
        
        return np.array(ps_points)

    @staticmethod
    def plot_poincare(ps_points, indices=(0, 1), labels=('x', 'v')):
        """
        Renders the Poincaré section. Identifies "islands around islands."
        """
        if len(ps_points) == 0:
            return

        plt.figure(figsize=(8, 8))
        plt.scatter(ps_points[:, indices[0]], ps_points[:, indices[1]], 
                    s=0.5, color='#ff3333', alpha=0.6)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.title("Poincaré Section: Topological Invariants")
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.show()