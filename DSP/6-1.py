import numpy as np
import matplotlib.pyplot as plt

# 定义连续时间信号的频率
f_c = 500  # Hz (1000π rad/s)
T_values = [1e-3, 0.1e-3, 0.01e-3]  # 采样间隔 (1ms, 0.1ms, 0.01ms)

# 采样点数
N = 1024  

plt.figure(figsize=(10, 6))

for i, T in enumerate(T_values):
    fs = 1 / T  # 采样频率
    n = np.arange(N)  # 采样点
    x_n = 2 * np.cos(1000 * np.pi * n * T)  # 采样信号

    # 计算DFT
    X_f = np.fft.fft(x_n, N)
    freqs = np.fft.fftfreq(N, d=T)  # 计算频率刻度
    X_f_magnitude = np.abs(X_f)  # 取振幅

    # 只绘制正频部分
    half_N = N // 2
    plt.subplot(3, 1, i+1)
    plt.plot(freqs[:half_N], X_f_magnitude[:half_N])
    plt.title(f"sampling period T = {T*1000:.3f} ms (sampling frequency fs = {fs:.1f} Hz)")
    plt.xlabel("frequency (Hz)")
    plt.ylabel("amplitude")

plt.tight_layout()
plt.show()