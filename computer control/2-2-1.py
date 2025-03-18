import numpy as np
import matplotlib.pyplot as plt

# 定义信号参数
A = 1
omega = 2 * np.pi * 1  # 假设 omega_1 = 2π * 1 Hz
omega1 = omega

# 定义采样频率
fs1 = 4 * omega1  # 第一种情况
fs2 = 1.5 * omega1  # 第二种情况

# 定义频率范围
frequencies = np.linspace(-5 * omega1, 5 * omega1, 1000)

# 原始信号的频谱
def original_spectrum(f):
    return (A/2) * (np.abs(f - omega) < 0.1) + (A/2) * (np.abs(f + omega) < 0.1)

# 采样后的频谱
def sampled_spectrum(f, fs):
    spectrum = np.zeros_like(f)
    for n in range(-5, 6):
        spectrum += original_spectrum(f - n * fs)
    return spectrum

# 理想滤波器
def ideal_filter(f, cutoff):
    return np.where(np.abs(f) <= cutoff, 1, 0)

# 绘制频谱
plt.figure(figsize=(12, 8))

# 原始频谱
plt.subplot(3, 1, 1)
plt.plot(frequencies, original_spectrum(frequencies), label='Original Spectrum')
plt.title('Original Signal Spectrum')
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Amplitude')
plt.legend()

# 采样频率为 4ω1
plt.subplot(3, 1, 2)
plt.plot(frequencies, sampled_spectrum(frequencies, fs1), label='Sampled Spectrum (fs=4ω1)')
plt.title('Sampled Signal Spectrum (fs=4ω1)')
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Amplitude')
plt.legend()

# 采样频率为 1.5ω1
plt.subplot(3, 1, 3)
plt.plot(frequencies, sampled_spectrum(frequencies, fs2), label='Sampled Spectrum (fs=1.5ω1)')
plt.title('Sampled Signal Spectrum (fs=1.5ω1)')
plt.xlabel('Frequency (rad/s)')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()