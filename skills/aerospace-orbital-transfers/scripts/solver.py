"""
Aerospace Orbital Mechanics & Staging Deterministic Solver
Computes Vis-Viva velocities, Hohmann transfer delta-v budgets, transfer times, and propellant mass ratios.
"""

import math
from typing import Dict, Any

# Earth standard gravitational constants
EARTH_MU = 3.986004418e14  # m^3/s^2
EARTH_RADIUS = 6371000.0   # m
STANDARD_G0 = 9.80665      # m/s^2

class OrbitalMechanicsSolver:
    @staticmethod
    def calculate_vis_viva(r: float, a: float, mu: float = EARTH_MU) -> float:
        """
        Calculates orbital speed in m/s.
        r: Current orbital radius from body center (m)
        a: Semi-major axis (m). Set a=r for circular orbit, a=inf for parabolic escape.
        """
        if math.isinf(a):
            return math.sqrt(2.0 * mu / r)
        return math.sqrt(mu * (2.0 / r - 1.0 / a))

    @staticmethod
    def calculate_hohmann_transfer(
        r1: float,
        r2: float,
        mu: float = EARTH_MU
    ) -> Dict[str, float]:
        """
        Calculates complete Hohmann transfer parameters between circular orbits r1 and r2.
        r1, r2: Radii in meters from body center.
        """
        v1_circ = math.sqrt(mu / r1)
        v2_circ = math.sqrt(mu / r2)

        a_tx = (r1 + r2) / 2.0
        v_tx_periapsis = math.sqrt(mu * (2.0 / r1 - 1.0 / a_tx))
        v_tx_apoapsis = math.sqrt(mu * (2.0 / r2 - 1.0 / a_tx))

        dv1 = abs(v_tx_periapsis - v1_circ)
        dv2 = abs(v2_circ - v_tx_apoapsis)
        total_dv = dv1 + dv2

        # Transfer time is half the orbital period of the transfer ellipse
        transfer_time_sec = math.pi * math.sqrt((a_tx ** 3) / mu)

        return {
            "r1_m": r1,
            "r2_m": r2,
            "v1_circ_mps": v1_circ,
            "v2_circ_mps": v2_circ,
            "delta_v1_mps": dv1,
            "delta_v2_mps": dv2,
            "total_delta_v_mps": total_dv,
            "transfer_time_sec": transfer_time_sec,
            "transfer_time_hours": transfer_time_sec / 3600.0
        }

    @staticmethod
    def calculate_rocket_staging(
        delta_v: float,
        isp_sec: float,
        dry_mass_kg: float,
        g0: float = STANDARD_G0
    ) -> Dict[str, float]:
        """
        Calculates required wet propellant mass via Tsiolkovsky equation.
        """
        mass_ratio = math.exp(delta_v / (isp_sec * g0))
        wet_mass_kg = dry_mass_kg * mass_ratio
        propellant_mass_kg = wet_mass_kg - dry_mass_kg
        return {
            "delta_v_mps": delta_v,
            "mass_ratio": mass_ratio,
            "dry_mass_kg": dry_mass_kg,
            "wet_mass_kg": wet_mass_kg,
            "propellant_mass_kg": propellant_mass_kg
        }

if __name__ == "__main__":
    # Test Fixture: LEO (300 km altitude) to GEO (42,164 km radius)
    r_leo = EARTH_RADIUS + 300000.0  # ~6,671,000 m
    r_geo = 42164000.0               # ~42,164,000 m

    hohmann = OrbitalMechanicsSolver.calculate_hohmann_transfer(r_leo, r_geo)
    print("✓ Hohmann Transfer LEO -> GEO:")
    print(f"  Delta-V 1: {hohmann['delta_v1_mps']:.2f} m/s")
    print(f"  Delta-V 2: {hohmann['delta_v2_mps']:.2f} m/s")
    print(f"  Total Delta-V: {hohmann['total_delta_v_mps']:.2f} m/s (~3.9 km/s expected)")
    print(f"  Transfer Time: {hohmann['transfer_time_hours']:.2f} hours (~5.27 hrs expected)")
    assert 3800 < hohmann['total_delta_v_mps'] < 4100
    assert 5.0 < hohmann['transfer_time_hours'] < 5.5

    # Rocket Staging: Hydrolox upper stage (Isp = 450s, Dry mass = 2500 kg)
    staging = OrbitalMechanicsSolver.calculate_rocket_staging(hohmann['total_delta_v_mps'], 450.0, 2500.0)
    print(f"✓ Upper Stage Propellant Needed: {staging['propellant_mass_kg']:.1f} kg")
    print("ALL TESTS PASSED for aerospace-orbital-transfers.")
