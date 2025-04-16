import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 信号的参数
N = 62  # 假设信号长度为62
n = np.arange(N)  # 时间序列

# 假设 R_62[n] 是一个单位脉冲信号或者你可以替换成任何其他信号
R_62 = np.ones(N)  # 这里选择单位脉冲作为示例

# 防止除零错误
n_shifted = n - 30.5

# 计算 h[n] 的值
h_n = (1 / 2) * np.sinc(0.02 * (n_shifted)) * (1 - np.cos(2 * np.pi * n / 61)) * R_62

# 绘制 h[n] 的幅度响应 |H(e^jw)|
# 计算 H(w) 的频率响应
h_n_fft = np.fft.fft(h_n, N)  # 计算离散傅里叶变换
frequencies = np.fft.fftfreq(N, 1)  # 获取频率轴

# 计算幅度响应 |H(e^jw)|
H_magnitude = np.abs(h_n_fft)

# 计算分贝表示 20 * log10(|H(e^jw)|)
H_dB = 20 * np.log10(H_magnitude + 1e-10)  # 加小量避免log(0)

# 绘图
plt.figure(figsize=(12, 6))

# 子图1：幅度响应 |H(e^jw)|
plt.subplot(2, 1, 1)
plt.plot(frequencies[:N//2], H_magnitude[:N//2], label=r'$|H(e^{j\omega})|$')
plt.title(r'$|H(e^{j\omega})|$ 幅度响应')
plt.xlabel(r'Frequency $\omega$ (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.legend()

# 子图2：分贝表示 20 * log10(|H(e^jw)|)
plt.subplot(2, 1, 2)
plt.plot(frequencies[:N//2], H_dB[:N//2], label=r'$20\log_{10}(|H(e^{j\omega})|)$')
plt.title(r'$|H(e^{j\omega})|$ 分贝表示')
plt.xlabel(r'Frequency $\omega$ (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# 显示所有子图
plt.tight_layout()
plt.show()
