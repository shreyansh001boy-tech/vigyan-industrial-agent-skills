---
name: biomedical-signal-filtering
description: Industrial biomedical engineering and bio-signal processing solver for ECG/EEG digital Butterworth bandpass filtering, powerline noise removal, and heart rate R-peak detection.
---

# Biomedical Bio-Signal Filtering & Conditioning Skill

## 1. Domain Background
In clinical patient monitors, ICU telemetry, and wearable medical devices, electrophysiological signals (ECG, EEG, EMG) have microvolt-to-millivolt amplitudes heavily corrupted by physiological and electrical noise:
* **Baseline wander (0.05–0.5 Hz):** Induced by respiration and patient movement.
* **Powerline interference (50 Hz or 60 Hz):** Induced by capacitive AC coupling to mains power.
* **Electromyographic (EMG) muscle noise (20–500 Hz):** High-frequency random spikes.

---

## 2. Governing Signal Processing Formulations

### 1. Diagnostic Bandpass Filtering (AHA Standards)
The American Heart Association (AHA) recommends:
* Highpass cutoff: $f_L \approx 0.5\text{ Hz}$ to eliminate baseline drift without distorting ST segments.
* Lowpass cutoff: $f_H \approx 40 - 150\text{ Hz}$ to preserve QRS complex fidelity while suppressing high-frequency noise.

### 2. Digital Butterworth Frequency Response
For an $N$-th order Butterworth filter:
$$|H(j\omega)|^2 = \frac{1}{1 + \left(\frac{\omega}{\omega_c}\right)^{2N}}$$
Characterized by a maximally flat passband with no ripple.

### 3. Signal-to-Noise Ratio (SNR)
$$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_{\text{clean}}}{P_{\text{noise}}}\right) = 10 \log_{10}\left(\frac{\sum x_i^2}{\sum (y_i - x_i)^2}\right)$$

### 4. Heart Rate Extraction from R-Peak Interval
$$\text{Heart Rate (BPM)} = \frac{60}{\Delta t_{RR}} = \frac{60 \cdot f_s}{N_{RR}}$$
where $f_s$ is sampling frequency (Hz) and $N_{RR}$ is sample interval between consecutive R peaks.

---

## 3. Procedural Agent Runbook
1. **Determine Sampling Rate $f_s$:** Ensure $f_s \ge 2 f_{\max}$ (Nyquist rate, typically 250–1000 Hz for ECG).
2. **Design Digital Bandpass Filter:** Compute 2nd to 4th order Butterworth filter coefficients ($b, a$).
3. **Filter Signal:** Apply zero-phase forward-backward filtering (`scipy.signal.filtfilt`) to eliminate phase delay.
4. **Detect Peaks & Metrics:** Extract R-peak intervals, heart rate in BPM, and post-filtering SNR.
