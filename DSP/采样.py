import numpy as np
import matplotlib.pyplot as plt

# 已知信号 x_c(t) = 2cos(1000πt)
F_c = 500  # 计算得到的信号频率 F = 1000π / (2π) = 500 Hz

# 采样间隔 T
T_values = [1e-3, 0.1e-3, 0.01e-3]  # T = 1ms, 0.1ms, 0.01ms
Fs_values = [1/T for T in T_values]  # 计算采样频率 F_s = 1/T

# 设置时间范围用于生成连续信号
t_continuous = np.linspace(0, 0.01, 1000)  # 取 10ms 时间范围
x_continuous = 2 * np.cos(1000 * np.pi * t_continuous)  # 生成连续信号

# 设置频率轴范围（显示多个周期以观察混叠）
num_periods = 3

# 创建子图
fig, axes = plt.subplots(3, 2, figsize=(12, 12))

for i, (T, Fs) in enumerate(zip(T_values, Fs_values)):
    # 计算采样点
    n = np.arange(0, 0.01, T)  # 采样点时间
    x_sampled = 2 * np.cos(1000 * np.pi * n)  # 采样后的信号
    
    # 频域分析：计算采样后频谱
    F_N = Fs / 2  # 奈奎斯特频率
    freqs = np.arange(-num_periods * Fs, num_periods * Fs, 1)  # 频率轴
    spectrum = np.zeros_like(freqs)  # 初始化频谱
    
    # 采样后频谱的周期延拓
    for k in range(-num_periods, num_periods + 1):  
        spectrum[np.abs(freqs - (F_c + k * Fs)) < 1] = 1
        spectrum[np.abs(freqs + (F_c + k * Fs)) < 1] = 1

    # 绘制时域信号
    axes[i, 0].plot(t_continuous, x_continuous, label="Continuous Signal")
    axes[i, 0].stem(n, x_sampled, linefmt='r-', markerfmt='ro', basefmt=" ", label="Sampled Points")
    axes[i, 0].set_xlabel("Time (s)")
    axes[i, 0].set_ylabel("Amplitude")
    axes[i, 0].set_title(f"Time Domain Signal (T = {T*1e3:.3f} ms, Fs = {Fs:.1f} Hz)")
    axes[i, 0].legend()
    axes[i, 0].grid()

    # 绘制频谱
    axes[i, 1].stem(freqs, spectrum, basefmt=" ")
    axes[i, 1].set_xlim(-num_periods * Fs, num_periods * Fs)
    axes[i, 1].set_ylim(0, 1.2)
    axes[i, 1].set_xlabel("Frequency (Hz)")
    axes[i, 1].set_ylabel("Magnitude")
    axes[i, 1].set_title(f"Sampled Spectrum (T = {T*1e3:.3f} ms, Fs = {Fs:.1f} Hz)")
    axes[i, 1].grid()

plt.tight_layout()
plt.show()