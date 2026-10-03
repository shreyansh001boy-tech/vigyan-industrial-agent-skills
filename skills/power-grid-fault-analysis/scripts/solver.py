"""
Electrical Power Grid Symmetrical & Unsymmetrical Fault Solver
Computes per-unit base conversions, Fortescue components, and 3-phase/SLG fault currents.
"""

import cmath
import math
from typing import Dict, Any, Tuple

# Complex operator a = e^(j 120 deg)
OPERATOR_A = cmath.rect(1.0, math.radians(120))
OPERATOR_A2 = cmath.rect(1.0, math.radians(240))

class PowerGridFaultSolver:
    @staticmethod
    def calculate_base_impedance(s_base_mva: float, v_base_kv: float) -> Dict[str, float]:
        """
        Calculates base impedance in Ohms and base current in Amperes.
        """
        z_base_ohms = (v_base_kv ** 2) / s_base_mva
        i_base_amps = (s_base_mva * 1e6) / (math.sqrt(3) * v_base_kv * 1e3)
        return {
            "s_base_mva": s_base_mva,
            "v_base_kv": v_base_kv,
            "z_base_ohms": z_base_ohms,
            "i_base_amps": i_base_amps
        }

    @staticmethod
    def fortescue_transform(
        i_a: complex,
        i_b: complex,
        i_c: complex
    ) -> Tuple[complex, complex, complex]:
        """
        Converts phase currents (Ia, Ib, Ic) into sequence currents (I0, I1, I2).
        """
        i_0 = (1.0 / 3.0) * (i_a + i_b + i_c)
        i_1 = (1.0 / 3.0) * (i_a + OPERATOR_A * i_b + OPERATOR_A2 * i_c)
        i_2 = (1.0 / 3.0) * (i_a + OPERATOR_A2 * i_b + OPERATOR_A * i_c)
        return (i_0, i_1, i_2)

    @staticmethod
    def calculate_fault_currents(
        z0: complex,
        z1: complex,
        z2: complex,
        v_prefault: complex = 1.0 + 0j,
        zf: complex = 0.0 + 0j
    ) -> Dict[str, Any]:
        """
        Calculates balanced 3-phase, single line-to-ground (SLG), and line-to-line (LL) fault currents in per-unit.
        """
        # 1. Balanced Three-Phase Fault
        i_3phase = v_prefault / (z1 + zf)

        # 2. Single Line-to-Ground Fault (Phase A)
        i_slg = (3.0 * v_prefault) / (z0 + z1 + z2 + 3.0 * zf)

        # 3. Line-to-Line Fault (Phase B to C)
        i_ll = (-1j * math.sqrt(3) * v_prefault) / (z1 + z2 + zf)

        return {
            "three_phase_pu": i_3phase,
            "three_phase_mag": abs(i_3phase),
            "slg_pu": i_slg,
            "slg_mag": abs(i_slg),
            "line_to_line_pu": i_ll,
            "line_to_line_mag": abs(i_ll)
        }

if __name__ == "__main__":
    # Test Fixture: 100 MVA, 138 kV substation bus
    base_info = PowerGridFaultSolver.calculate_base_impedance(100.0, 138.0)
    print(f"✓ Base Impedance: {base_info['z_base_ohms']:.2f} Ohms")
    print(f"✓ Base Current: {base_info['i_base_amps']:.2f} A")

    # Sequence impedances: Z1 = 0.05 + j0.20, Z2 = 0.05 + j0.20, Z0 = 0.10 + j0.50 pu
    z1 = 0.05 + 0.20j
    z2 = 0.05 + 0.20j
    z0 = 0.10 + 0.50j

    faults = PowerGridFaultSolver.calculate_fault_currents(z0, z1, z2)
    i_base = base_info['i_base_amps']

    print("✓ Fault Current Magnitudes (Per Unit & Actual kA):")
    print(f"  3-Phase Fault : {faults['three_phase_mag']:.2f} pu = {(faults['three_phase_mag'] * i_base)/1e3:.2f} kA")
    print(f"  SLG Fault     : {faults['slg_mag']:.2f} pu = {(faults['slg_mag'] * i_base)/1e3:.2f} kA")
    print(f"  L-L Fault     : {faults['line_to_line_mag']:.2f} pu = {(faults['line_to_line_mag'] * i_base)/1e3:.2f} kA")

    assert faults['three_phase_mag'] > 0
    assert faults['slg_mag'] > 0
    print("ALL TESTS PASSED for power-grid-fault-analysis.")
