"""
Materials Science & Crystal Diffraction Deterministic Solver
Computes Bragg's law d-spacings, cubic lattice constants, crystal densities, and Vegard's law bandgap tuning.
"""

import math
from typing import Dict, Any

AVOGADRO = 6.02214076e23  # atoms / mol
CU_K_ALPHA_WAVELENGTH_ANGSTROM = 1.5406  # Angstroms

class CrystallographySolver:
    @staticmethod
    def calculate_bragg_d_spacing(
        two_theta_degrees: float,
        wavelength_angstrom: float = CU_K_ALPHA_WAVELENGTH_ANGSTROM,
        order_n: int = 1
    ) -> Dict[str, float]:
        """
        Calculates interplanar d-spacing from XRD 2-theta angle.
        """
        theta_rad = math.radians(two_theta_degrees / 2.0)
        sin_theta = math.sin(theta_rad)
        if sin_theta <= 0:
            return {"error": "Invalid diffraction angle"}

        d_angstrom = (order_n * wavelength_angstrom) / (2.0 * sin_theta)
        return {
            "two_theta_deg": two_theta_degrees,
            "theta_deg": two_theta_degrees / 2.0,
            "wavelength_angstrom": wavelength_angstrom,
            "d_spacing_angstrom": d_angstrom,
            "d_spacing_nm": d_angstrom / 10.0
        }

    @staticmethod
    def calculate_cubic_lattice_constant(
        d_spacing_angstrom: float,
        h: int, k: int, l: int
    ) -> float:
        """
        Calculates unit cell lattice constant 'a' for a cubic crystal given Miller indices (h, k, l).
        """
        factor = math.sqrt(h**2 + k**2 + l**2)
        return d_spacing_angstrom * factor

    @staticmethod
    def calculate_vegard_alloy(
        x_fraction: float,
        a_ac: float,
        a_bc: float,
        eg_ac_ev: float,
        eg_bc_ev: float,
        bowing_b: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculates lattice constant and bandgap for ternary alloy A_(1-x) B_x C using Vegard's law.
        """
        x = x_fraction
        a_alloy = (1.0 - x) * a_ac + x * a_bc
        eg_linear = (1.0 - x) * eg_ac_ev + x * eg_bc_ev
        eg_alloy = eg_linear - bowing_b * x * (1.0 - x)

        return {
            "x_fraction": x,
            "lattice_constant_angstrom": a_alloy,
            "bandgap_ev": eg_alloy,
            "emission_wavelength_nm": (1239.84 / eg_alloy) if eg_alloy > 0 else 0.0
        }

if __name__ == "__main__":
    # Test Fixture: Silicon (111) peak with Cu-K-alpha (2-theta = 28.44 degrees)
    xrd = CrystallographySolver.calculate_bragg_d_spacing(28.44)
    d_111 = xrd["d_spacing_angstrom"]
    print(f"✓ Si (111) d-spacing: {d_111:.4f} Angstroms (~3.1355 Angstroms expected)")
    assert abs(d_111 - 3.1355) < 0.01

    # Silicon lattice constant a = d_111 * sqrt(1^2 + 1^2 + 1^2) = d * sqrt(3)
    a_si = CrystallographySolver.calculate_cubic_lattice_constant(d_111, 1, 1, 1)
    print(f"✓ Silicon Unit Cell Parameter a: {a_si:.4f} Angstroms (~5.431 Angstroms expected)")
    assert abs(a_si - 5.431) < 0.02

    # In_x Ga_(1-x) As alloy for telecomm 1550 nm laser: InAs (a=6.058A, Eg=0.36eV), GaAs (a=5.653A, Eg=1.42eV)
    # Target In_0.53 Ga_0.47 As matched to InP
    alloy = CrystallographySolver.calculate_vegard_alloy(0.53, 5.653, 6.058, 1.42, 0.36, bowing_b=0.475)
    print(f"✓ In0.53Ga0.47As Lattice Constant: {alloy['lattice_constant_angstrom']:.4f} A (~5.868 A expected)")
    print(f"✓ In0.53Ga0.47As Bandgap: {alloy['bandgap_ev']:.3f} eV (~0.74 eV expected)")
    assert abs(alloy['lattice_constant_angstrom'] - 5.868) < 0.02
    assert abs(alloy['bandgap_ev'] - 0.74) < 0.05
    print("ALL TESTS PASSED for materials-crystal-diffraction.")
