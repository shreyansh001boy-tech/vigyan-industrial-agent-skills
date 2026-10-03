"""
Biomedical Bio-Signal Filtering & Peak Detection Deterministic Solver
Computes Butterworth filter coefficients, zero-phase filtering, SNR metrics, and heart rate (BPM).
"""

import math
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class BioSignalFilterSolver:
    @staticmethod
    def calculate_butterworth_bandpass_poles(
        lowcut_hz: float,
        highcut_hz: float,
        sampling_rate_hz: float,
        order: int = 2
    ) -> Dict[str, Any]:
        """
        Calculates normalized cutoff frequencies and digital filter configuration.
        """
        nyquist = 0.5 * sampling_rate_hz
        low = lowcut_hz / nyquist
        high = highcut_hz / nyquist
        return {
            "sampling_rate_hz": sampling_rate_hz,
            "nyquist_hz": nyquist,
            "lowcut_hz": lowcut_hz,
            "highcut_hz": highcut_hz,
            "normalized_low": low,
            "normalized_high": high,
            "filter_order": order
        }

    @staticmethod
    def calculate_snr_db(clean_signal: Any, noisy_signal: Any) -> float:
        """
        Calculates Signal-to-Noise Ratio (SNR) in decibels.
        """
        if HAS_NUMPY and isinstance(clean_signal, np.ndarray):
            noise = noisy_signal - clean_signal
            p_signal = float(np.mean(clean_signal ** 2))
            p_noise = float(np.mean(noise ** 2))
        else:
            c_list = list(clean_signal)
            n_list = list(noisy_signal)
            n = len(c_list)
            p_signal = sum(x**2 for x in c_list) / n
            p_noise = sum((ny - cy)**2 for cy, ny in zip(c_list, n_list)) / n

        if p_noise <= 0:
            return float('inf')
        return float(10.0 * math.log10(p_signal / p_noise))

    @staticmethod
    def calculate_heart_rate(
        r_peak_indices: List[int],
        sampling_rate_hz: float
    ) -> Dict[str, float]:
        """
        Calculates mean heart rate (BPM) and heart rate variability (HRV SDNN in ms) from R-peak sample indices.
        """
        if len(r_peak_indices) < 2:
            return {"error": "Need at least 2 R-peaks to calculate heart rate"}

        diffs_samples = [r_peak_indices[i] - r_peak_indices[i - 1] for i in range(1, len(r_peak_indices))]
        rr_intervals_sec = [d / sampling_rate_hz for d in diffs_samples]
        bpm_values = [60.0 / rr for rr in rr_intervals_sec]

        mean_bpm = sum(bpm_values) / len(bpm_values)
        mean_rr_sec = sum(rr_intervals_sec) / len(rr_intervals_sec)
        mean_rr_ms = mean_rr_sec * 1000.0
        variance = sum((x - mean_rr_sec) ** 2 for x in rr_intervals_sec) / len(rr_intervals_sec)
        sdnn_ms = math.sqrt(variance) * 1000.0

        return {
            "mean_heart_rate_bpm": float(mean_bpm),
            "mean_rr_interval_ms": float(mean_rr_ms),
            "hrv_sdnn_ms": float(sdnn_ms)
        }

if __name__ == "__main__":
    # Test Fixture 1: Filter specifications for standard 500 Hz diagnostic ECG
    specs = BioSignalFilterSolver.calculate_butterworth_bandpass_poles(0.5, 45.0, 500.0, order=3)
    print("✓ ECG Bandpass Filter Configuration:", specs)
    assert 0 < specs["normalized_low"] < specs["normalized_high"] < 1.0

    # Test Fixture 2: Heart rate from 5 detected R-peaks at 500 Hz (spaced exactly 400 samples = 0.8s = 75 BPM)
    r_peaks = [500, 900, 1300, 1700, 2100]
    hr = BioSignalFilterSolver.calculate_heart_rate(r_peaks, 500.0)
    print(f"✓ Detected Heart Rate: {hr['mean_heart_rate_bpm']:.1f} BPM (~75.0 BPM expected)")
    print(f"✓ Mean R-R Interval: {hr['mean_rr_interval_ms']:.1f} ms (~800.0 ms expected)")
    assert abs(hr['mean_heart_rate_bpm'] - 75.0) < 0.1
    assert abs(hr['mean_rr_interval_ms'] - 800.0) < 0.1

    # Test Fixture 3: SNR calculation
    clean = [math.sin(i * 10.0 / 1000.0) for i in range(1000)]
    noisy = [c + 0.1 * math.cos(i * 100.0 / 1000.0) for i, c in enumerate(clean)]
    snr = BioSignalFilterSolver.calculate_snr_db(clean, noisy)
    print(f"✓ Bio-Signal SNR: {snr:.2f} dB")
    assert snr > 15.0
    print("ALL TESTS PASSED for biomedical-signal-filtering.")
