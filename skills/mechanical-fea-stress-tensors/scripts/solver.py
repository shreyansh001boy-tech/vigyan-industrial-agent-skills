"""
Mechanical FEA Stress Tensors & Yield Failure Deterministic Solver
Computes 3D principal stresses, stress invariants, von Mises equivalent stress, and beam deflections.
"""

import math
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
from typing import Dict, Any, List

class StressTensorSolver:
    @staticmethod
    def calculate_von_mises(
        s_xx: float, s_yy: float, s_zz: float,
        t_xy: float, t_yz: float, t_xz: float,
        yield_strength: float = None
    ) -> Dict[str, Any]:
        """
        Computes 3D principal stresses and von Mises equivalent stress.
        Values in Pascals (or consistent MPa).
        """
        # Calculate von Mises
        term1 = (s_xx - s_yy) ** 2
        term2 = (s_yy - s_zz) ** 2
        term3 = (s_zz - s_xx) ** 2
        term_shear = 6.0 * (t_xy**2 + t_yz**2 + t_xz**2)
        von_mises = math.sqrt(0.5 * (term1 + term2 + term3 + term_shear))

        if HAS_NUMPY:
            # Construct symmetric stress tensor matrix
            sigma_mat = np.array([
                [s_xx, t_xy, t_xz],
                [t_xy, s_yy, t_yz],
                [t_xz, t_yz, s_zz]
            ], dtype=float)
            eigenvalues = np.linalg.eigvalsh(sigma_mat)
            sorted_principals = [float(x) for x in np.sort(eigenvalues)[::-1]]
        else:
            # Analytical Haigh-Westergaard / deviatoric stress invariants
            i1 = s_xx + s_yy + s_zz
            mean_s = i1 / 3.0
            sx, sy, sz = s_xx - mean_s, s_yy - mean_s, s_zz - mean_s
            j2 = 0.5 * (sx**2 + sy**2 + sz**2) + t_xy**2 + t_yz**2 + t_xz**2
            if j2 < 1e-12:
                sorted_principals = [mean_s, mean_s, mean_s]
            else:
                j3 = (sx * (sy * sz - t_yz**2) - 
                      t_xy * (t_xy * sz - t_yz * t_xz) + 
                      t_xz * (t_xy * t_yz - sy * t_xz))
                arg = (3.0 * math.sqrt(3.0) / 2.0) * (j3 / (j2 ** 1.5))
                arg = max(-1.0, min(1.0, arg))
                theta = math.acos(arg) / 3.0
                r = 2.0 * math.sqrt(j2 / 3.0)
                p1 = mean_s + r * math.cos(theta)
                p2 = mean_s + r * math.cos(theta - 2.0 * math.pi / 3.0)
                p3 = mean_s + r * math.cos(theta + 2.0 * math.pi / 3.0)
                sorted_principals = sorted([p1, p2, p3], reverse=True)

        fos = (yield_strength / von_mises) if (yield_strength and von_mises > 0) else None
        will_yield = (von_mises >= yield_strength) if yield_strength else None

        return {
            "principal_stresses": [float(s) for s in sorted_principals],
            "von_mises_stress": float(von_mises),
            "yield_strength": yield_strength,
            "factor_of_safety": float(fos) if fos else None,
            "yielding_predicted": will_yield
        }

    @staticmethod
    def calculate_cantilever_deflection(
        load_newtons: float,
        length_meters: float,
        youngs_modulus_pascals: float,
        second_moment_m4: float
    ) -> Dict[str, float]:
        """
        Computes max end deflection and max bending moment for a point-loaded cantilever.
        """
        p = load_newtons
        l = length_meters
        e = youngs_modulus_pascals
        i = second_moment_m4

        max_deflection_m = (p * (l ** 3)) / (3.0 * e * i)
        max_moment_nm = p * l

        return {
            "load_n": p,
            "length_m": l,
            "max_deflection_m": max_deflection_m,
            "max_deflection_mm": max_deflection_m * 1e3,
            "max_bending_moment_nm": max_moment_nm
        }

if __name__ == "__main__":
    # Test Fixture: Combined tension and torsion in shaft
    # sigma_xx = 120 MPa, tau_xy = 70 MPa, all other components 0. Yield = 250 MPa (Steel)
    res = StressTensorSolver.calculate_von_mises(120.0, 0.0, 0.0, 70.0, 0.0, 0.0, yield_strength=250.0)
    print(f"✓ Principal Stresses: {res['principal_stresses']} MPa")
    print(f"✓ von Mises Stress: {res['von_mises_stress']:.2f} MPa")
    print(f"✓ Factor of Safety: {res['factor_of_safety']:.2f}")
    # Analytical von Mises for uniaxial sigma + pure shear tau is sqrt(sigma^2 + 3*tau^2)
    # sqrt(120^2 + 3*70^2) = sqrt(14400 + 14700) = sqrt(29100) = 170.587 MPa
    expected_vm = math.sqrt(120.0**2 + 3.0 * 70.0**2)
    assert abs(res['von_mises_stress'] - expected_vm) < 0.01
    assert res['yielding_predicted'] is False

    # Cantilever test: 1000 N load, 2.0 m long steel beam (E=200 GPa, I=1e-5 m^4)
    beam = StressTensorSolver.calculate_cantilever_deflection(1000.0, 2.0, 200.0e9, 1.0e-5)
    print(f"✓ Cantilever Tip Deflection: {beam['max_deflection_mm']:.2f} mm")
    # delta = (1000 * 8) / (3 * 200e9 * 1e-5) = 8000 / 6e6 = 0.001333 m = 1.33 mm
    assert abs(beam['max_deflection_mm'] - 1.333) < 0.05
    print("ALL TESTS PASSED for mechanical-fea-stress-tensors.")
