"""
VLSI CMOS Timing Closure & Leakage Power Deterministic Solver
Computes setup/hold slacks, Elmore RC propagation delay, and dynamic/leakage power.
"""

from typing import List, Tuple, Dict, Any

class VLSITimingSolver:
    @staticmethod
    def calculate_elmore_delay(segments: List[Tuple[float, float]]) -> float:
        """
        Calculates Elmore delay for an RC ladder.
        segments: List of tuples [(R1, C1), (R2, C2), ...] where R is in Ohms, C is in Farads.
        Returns: Delay in seconds.
        """
        total_delay = 0.0
        n = len(segments)
        for i in range(n):
            r_i = segments[i][0]
            downstream_c = sum(segments[j][1] for j in range(i, n))
            total_delay += r_i * downstream_c
        return total_delay

    @staticmethod
    def calculate_slack(
        t_clk: float,
        t_cq: float,
        t_comb: float,
        t_setup: float,
        t_hold: float,
        t_skew: float = 0.0
    ) -> Dict[str, Any]:
        """
        Computes setup and hold timing slacks in seconds (or picoseconds if consistent).
        """
        setup_slack = t_clk - (t_cq + t_comb + t_setup) + t_skew
        hold_slack = (t_cq + t_comb) - t_hold - t_skew
        return {
            "setup_slack_sec": setup_slack,
            "setup_violation": setup_slack < 0.0,
            "hold_slack_sec": hold_slack,
            "hold_violation": hold_slack < 0.0,
            "max_frequency_hz": 1.0 / (t_cq + t_comb + t_setup - t_skew) if (t_cq + t_comb + t_setup - t_skew) > 0 else 0.0
        }

    @staticmethod
    def calculate_power(
        activity_factor: float,
        load_capacitance: float,
        v_dd: float,
        frequency_hz: float,
        leakage_current_amps: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculates dynamic, static leakage, and total power in Watts.
        """
        p_dyn = activity_factor * load_capacitance * (v_dd ** 2) * frequency_hz
        p_leak = leakage_current_amps * v_dd
        return {
            "p_dynamic_watts": p_dyn,
            "p_leakage_watts": p_leak,
            "p_total_watts": p_dyn + p_leak
        }

if __name__ == "__main__":
    # Test Fixture: 1 GHz clock (1ns = 1e-9s), 28nm standard cell
    t_clk = 1.0e-9
    t_cq = 0.12e-9
    t_comb = 0.65e-9
    t_setup = 0.10e-9
    t_hold = 0.05e-9
    t_skew = 0.02e-9

    slack_res = VLSITimingSolver.calculate_slack(t_clk, t_cq, t_comb, t_setup, t_hold, t_skew)
    print("✓ Timing Slack Test:", slack_res)
    assert slack_res["setup_slack_sec"] > 0, "Setup slack failed"
    assert slack_res["hold_slack_sec"] > 0, "Hold slack failed"

    # Elmore Delay Test: 3-stage interconnect
    rc_ladder = [(100.0, 50.0e-15), (150.0, 30.0e-15), (200.0, 20.0e-15)]
    elmore = VLSITimingSolver.calculate_elmore_delay(rc_ladder)
    print(f"✓ Elmore Delay: {elmore*1e12:.2f} ps")
    assert elmore > 0

    power = VLSITimingSolver.calculate_power(0.15, 10.0e-12, 0.9, 1.0e9, 50.0e-6)
    print(f"✓ Power Dissipation: {power['p_total_watts']*1e3:.2f} mW")
    print("ALL TESTS PASSED for vlsi-cmos-timing-closure.")
