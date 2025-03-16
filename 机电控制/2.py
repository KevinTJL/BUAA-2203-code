import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Define the original signal parameters
f0 = 10  # Hz
T_total = 1  # Total duration of the signal (1 second)
t_continuous = np.linspace(0, T_total, 1000)  # High-resolution time
y_continuous = np.sin(2 * np.pi * f0 * t_continuous)  # Original signal

# Define sampling frequencies
sampling_frequencies = [25, 15, 9.5, 30]  # Corresponding to each scenario
titles = [
    "Accurate Sampling (fs = 25 Hz)",
    "Aliasing (fs = 15 Hz)",
    "Beat Phenomenon (fs = 9.5 Hz)",
    "Hidden Oscillations (fs = 30 Hz)"
]

plt.figure(figsize=(12, 8))

# Time-domain plots for different sampling rates
for i, fs in enumerate(sampling_frequencies):
    Ts = 1 / fs  # Sampling period
    t_samples = np.arange(0, T_total, Ts)  # Sampled time points
    y_samples = np.sin(2 * np.pi * f0 * t_samples)  # Sampled signal

    plt.subplot(4, 2, 2 * i + 1)
    plt.plot(t_continuous, y_continuous, label="Original Signal", linestyle="dashed")
    plt.scatter(t_samples, y_samples, color="red", label="Sampled Points")
    plt.title(f"Time Domain: {titles[i]}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()

    # Compute Fourier Transform of sampled signal
    N = len(t_samples)
    Y_fft = fft(y_samples, 1024)
    freqs = fftfreq(1024, Ts)[:512]  # Only positive frequencies
    Y_magnitude = np.abs(Y_fft[:512])  # Take the magnitude

    plt.subplot(4, 2, 2 * i + 2)
    plt.plot(freqs, Y_magnitude, label="Magnitude Spectrum")
    plt.title(f"Frequency Spectrum: {titles[i]}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, 50)  # Limit x-axis for better visualization
    plt.legend()

plt.tight_layout()
plt.show()
