import numpy as np
import matplotlib.pyplot as plt

# 定义参数
Fs = 100  # 采样频率
Ts = 1 / Fs  # 采样周期
t = np.arange(0, 1, Ts)  # 采样时间点
xc_t = 1 + np.cos(10 * np.pi * t)  # 采样得到的序列 x[n]

# 绘制 x[n]
plt.figure(figsize=(12, 5))
plt.stem(t, xc_t, linefmt='b-', markerfmt='bo', basefmt="r-")
plt.xlabel('Time (s)')
plt.ylabel('x[n]')
plt.title('Sampled Signal x[n]')
plt.grid()
plt.show()

# 计算频谱 X(e^jω)
N = 256  # 频谱点数
omega = np.linspace(-np.pi, np.pi, N)
X_w = np.fft.fftshift(np.fft.fft(xc_t, N))  # 计算 DTFT 近似值
X_w_magnitude = np.abs(X_w)  # 取幅度

# 绘制频谱 |X(e^jω)|
plt.figure(figsize=(12, 5))
plt.plot(omega, X_w_magnitude, 'b')
plt.xlabel('Frequency (rad/sample)')
plt.ylabel('|X(e^jω)|')
plt.title('Magnitude Spectrum of x[n]')
plt.grid()
plt.show()