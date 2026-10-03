"""
Robotics Forward Kinematics & State-Space Control Deterministic Solver
Computes Denavit-Hartenberg (DH) homogeneous transforms and state-space controllability matrices.
"""

import math
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
from typing import List, Dict, Any

def _mat_mult(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    r_a, c_a = len(a), len(a[0])
    c_b = len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(c_a)) for j in range(c_b)] for i in range(r_a)]

def _matrix_rank(matrix: List[List[float]], tol: float = 1e-9) -> int:
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot_row = None
        for r in range(rank, rows):
            if abs(a[r][col]) > tol:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        a[rank], a[pivot_row] = a[pivot_row], a[rank]
        pivot_val = a[rank][col]
        for c in range(col, cols):
            a[rank][c] /= pivot_val
        for r in range(rows):
            if r != rank and abs(a[r][col]) > tol:
                factor = a[r][col]
                for c in range(col, cols):
                    a[r][c] -= factor * a[rank][c]
        rank += 1
        if rank == rows:
            break
    return rank

class RoboticsControlSolver:
    @staticmethod
    def dh_matrix(theta_rad: float, d: float, a: float, alpha_rad: float) -> List[List[float]]:
        """
        Computes standard 4x4 DH transformation matrix for a single link.
        """
        ct = math.cos(theta_rad)
        st = math.sin(theta_rad)
        ca = math.cos(alpha_rad)
        sa = math.sin(alpha_rad)

        return [
            [ct, -st * ca,  st * sa, a * ct],
            [st,  ct * ca, -ct * sa, a * st],
            [0.0,      sa,       ca,      d],
            [0.0,     0.0,      0.0,    1.0]
        ]

    @staticmethod
    def forward_kinematics(dh_params: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Computes the end-effector transform for an n-DOF arm.
        dh_params: List of dicts with keys 'theta', 'd', 'a', 'alpha' (angles in radians).
        """
        t_total = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
        for p in dh_params:
            t_link = RoboticsControlSolver.dh_matrix(p["theta"], p["d"], p["a"], p["alpha"])
            t_total = _mat_mult(t_total, t_link)

        pos = [t_total[0][3], t_total[1][3], t_total[2][3]]
        rot = [row[:3] for row in t_total[:3]]
        return {
            "end_effector_position": pos,
            "rotation_matrix": rot,
            "full_transform": t_total
        }

    @staticmethod
    def check_controllability(a_mat: Any, b_mat: Any) -> Dict[str, Any]:
        """
        Computes the controllability matrix C = [B, AB, A^2B, ... A^(n-1)B] and checks rank.
        """
        if HAS_NUMPY and isinstance(a_mat, np.ndarray) and isinstance(b_mat, np.ndarray):
            n = a_mat.shape[0]
            c_blocks = [b_mat]
            current_ab = b_mat
            for _ in range(1, n):
                current_ab = np.dot(a_mat, current_ab)
                c_blocks.append(current_ab)
            c_mat = np.hstack(c_blocks)
            rank = int(np.linalg.matrix_rank(c_mat))
            return {
                "controllability_matrix": c_mat.tolist(),
                "matrix_rank": rank,
                "system_order": n,
                "is_controllable": (rank == n)
            }
        else:
            a_list = [list(row) for row in a_mat]
            b_list = [list(row) for row in b_mat]
            n = len(a_list)
            # Build C by horizontal stacking: C = [B, A*B, ...]
            blocks = [b_list]
            cur = b_list
            for _ in range(1, n):
                cur = _mat_mult(a_list, cur)
                blocks.append(cur)
            # Stack horizontally: each row i is concatenation of blocks[0][i], blocks[1][i], etc.
            c_mat = []
            for r in range(n):
                row_combined = []
                for b_idx in range(n):
                    row_combined.extend(blocks[b_idx][r])
                c_mat.append(row_combined)
            rank = _matrix_rank(c_mat)
            return {
                "controllability_matrix": c_mat,
                "matrix_rank": rank,
                "system_order": n,
                "is_controllable": (rank == n)
            }

if __name__ == "__main__":
    # Test Fixture 1: 2-link planar arm (a1=1.0m, a2=0.8m, theta1=30 deg, theta2=45 deg)
    th1 = math.radians(30)
    th2 = math.radians(45)
    planar_arm = [
        {"theta": th1, "d": 0.0, "a": 1.0, "alpha": 0.0},
        {"theta": th2, "d": 0.0, "a": 0.8, "alpha": 0.0}
    ]
    fk = RoboticsControlSolver.forward_kinematics(planar_arm)
    x, y, z = fk["end_effector_position"]
    print(f"✓ 2-Link Planar Forward Kinematics End-Effector: x={x:.3f}m, y={y:.3f}m, z={z:.3f}m")
    # Expected analytical x = 1.0*cos(30) + 0.8*cos(75) = 0.866 + 0.207 = 1.073m
    assert abs(x - 1.073) < 0.05
    assert abs(z) < 1e-9

    # Test Fixture 2: 2nd order inverted pendulum state-space model
    a = [[0.0, 1.0], [9.81, 0.0]]
    b = [[0.0], [1.0]]
    ctrl = RoboticsControlSolver.check_controllability(a, b)
    print(f"✓ State-Space Controllability: Rank={ctrl['matrix_rank']}/{ctrl['system_order']}, Controllable={ctrl['is_controllable']}")
    assert ctrl["is_controllable"] is True
    print("ALL TESTS PASSED for robotics-kinematics-control.")
