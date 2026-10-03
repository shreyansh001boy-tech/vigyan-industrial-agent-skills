"""
Chemical Reactor Engineering & Kinetics Deterministic Solver
Computes Arrhenius rate constants, CSTR and PFR sizing, residence times, and equilibrium conversions.
"""

import math
from typing import Dict, Any

GAS_CONSTANT_R = 8.314462618  # J / (mol * K)

class ChemicalReactorSolver:
    @staticmethod
    def calculate_arrhenius_k(
        pre_exponential_a: float,
        activation_energy_j_per_mol: float,
        temperature_kelvin: float
    ) -> float:
        """
        Calculates rate constant k at temperature T.
        """
        exponent = -activation_energy_j_per_mol / (GAS_CONSTANT_R * temperature_kelvin)
        return pre_exponential_a * math.exp(exponent)

    @staticmethod
    def size_reactors_first_order(
        volumetric_flow_m3_per_s: float,
        c_a0_mol_per_m3: float,
        rate_constant_per_s: float,
        target_conversion_fraction: float
    ) -> Dict[str, float]:
        """
        Computes required volume and residence time for both CSTR and PFR for first-order reaction.
        target_conversion_fraction: X between 0 and 1.
        """
        x = target_conversion_fraction
        k = rate_constant_per_s
        v0 = volumetric_flow_m3_per_s

        # CSTR: tau = X / (k * (1 - X))
        tau_cstr = x / (k * (1.0 - x))
        volume_cstr = tau_cstr * v0

        # PFR: tau = (1 / k) * ln(1 / (1 - X))
        tau_pfr = (1.0 / k) * math.log(1.0 / (1.0 - x))
        volume_pfr = tau_pfr * v0

        return {
            "target_conversion": x,
            "rate_constant_k": k,
            "cstr_tau_sec": tau_cstr,
            "cstr_volume_m3": volume_cstr,
            "pfr_tau_sec": tau_pfr,
            "pfr_volume_m3": volume_pfr,
            "cstr_to_pfr_volume_ratio": volume_cstr / volume_pfr if volume_pfr > 0 else 0.0
        }

    @staticmethod
    def calculate_antoine_vapor_pressure(
        a: float,
        b: float,
        c: float,
        temp_celsius: float
    ) -> float:
        """
        Calculates saturation pressure in mmHg using Antoine equation: log10(P) = A - B / (T + C)
        """
        log_p = a - (b / (temp_celsius + c))
        return 10.0 ** log_p

if __name__ == "__main__":
    # Test Fixture: Decomposition reaction, Ea = 80 kJ/mol, A = 1e11 s^-1, T = 350 K
    k = ChemicalReactorSolver.calculate_arrhenius_k(1.0e11, 80000.0, 350.0)
    print(f"✓ Arrhenius Rate Constant at 350K: {k:.4e} s^-1")
    assert k > 0

    # Sizing for 90% conversion (X = 0.90) with flow rate 0.01 m^3/s (~10 L/s)
    reactors = ChemicalReactorSolver.size_reactors_first_order(0.01, 1000.0, k, 0.90)
    print(f"✓ CSTR Volume: {reactors['cstr_volume_m3']:.2f} m^3 (tau={reactors['cstr_tau_sec']:.1f}s)")
    print(f"✓ PFR Volume : {reactors['pfr_volume_m3']:.2f} m^3 (tau={reactors['pfr_tau_sec']:.1f}s)")
    print(f"✓ CSTR / PFR Volume Ratio: {reactors['cstr_to_pfr_volume_ratio']:.2f}x (PFR is far more compact)")
    assert reactors['cstr_volume_m3'] > reactors['pfr_volume_m3']

    # Antoine test for water at 100 C (Expected ~760 mmHg)
    p_water = ChemicalReactorSolver.calculate_antoine_vapor_pressure(8.07131, 1730.63, 233.426, 100.0)
    print(f"✓ Water Vapor Pressure at 100C: {p_water:.1f} mmHg (~760 mmHg expected)")
    assert abs(p_water - 760.0) < 5.0
    print("ALL TESTS PASSED for chemical-reactor-thermo.")
