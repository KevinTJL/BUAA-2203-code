import numpy as np
import matplotlib.pyplot as plt

# 设定参数
A = 1
omega_1 = 1  # 设定 ω1 = 1 进行归一化
omega_s1 = 4 * omega_1  # 采样频率 4ω1
omega_s2 = 1.5 * omega_1  # 采样频率 1.5ω1

# 频率范围
omega = np.linspace(-5 * omega_1, 5 * omega_1, 1000)

# 原信号频谱
X_w = np.zeros_like(omega)
X_w[np.abs(omega - omega_1) < 0.05] = A/2
X_w[np.abs(omega + omega_1) < 0.05] = A/2

# 采样后频谱（4ω1）
X_s1 = np.zeros_like(omega)
for k in range(-2, 3):
    X_s1[np.abs(omega - omega_1 - k * omega_s1) < 0.05] = A/2
    X_s1[np.abs(omega + omega_1 - k * omega_s1) < 0.05] = A/2

# 采样后频谱（1.5ω1）
X_s2 = np.zeros_like(omega)
for k in range(-3, 4):
    X_s2[np.abs(omega - omega_1 - k * omega_s2) < 0.05] = A/2
    X_s2[np.abs(omega + omega_1 - k * omega_s2) < 0.05] = A/2

# 绘图
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# 原始信号频谱
axs[0].stem(omega, X_w, linefmt='b-', markerfmt='bo', basefmt="r-")
axs[0].set_title("Original Signal Spectrum")
axs[0].set_xlabel("Frequency (rad/s)")
axs[0].set_ylabel("Magnitude")
axs[0].grid()

# 采样频率 4ω1
axs[1].stem(omega, X_s1, linefmt='g-', markerfmt='go', basefmt="r-")
axs[1].set_title("Sampled Spectrum with Fs = 4ω1/2π")
axs[1].set_xlabel("Frequency (rad/s)")
axs[1].set_ylabel("Magnitude")
axs[1].grid()

# 采样频率 1.5ω1
axs[2].stem(omega, X_s2, linefmt='r-', markerfmt='ro', basefmt="r-")
axs[2].set_title("Sampled Spectrum with Fs = 1.5ω1/2π (Aliasing)")
axs[2].set_xlabel("Frequency (rad/s)")
axs[2].set_ylabel("Magnitude")
axs[2].grid()

plt.tight_layout()
plt.show()