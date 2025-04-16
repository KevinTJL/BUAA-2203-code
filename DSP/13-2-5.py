import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 信号的参数
N = 310  # 假设信号长度为310
n = np.arange(N)  # 时间序列

# 假设 R_310[n] 是一个单位脉冲信号或者你可以替换成任何其他信号
R_310 = np.ones(N)  # 这里选择单位脉冲作为示例

# 防止除零错误
n_shifted = n - 154.5

# 计算 h[n] 的值
h_n = (1 / 2) * np.sinc(0.02 * (n_shifted)) * (1 - np.cos(2 * np.pi * n / 309)) * R_310

# 绘制 h[n] 波形
plt.figure(figsize=(12, 6))

# 子图1：h[n]波形
plt.subplot(3, 1, 1)
plt.plot(n, h_n, label=r'$h[n] = \frac{1}{2} \cdot \frac{\sin(0.02\pi (n - 154.5))}{\pi (n - 154.5)} \cdot (1 - \cos\left( \frac{2\pi n}{309} \right)) \cdot R_{310}[n]$')
plt.title(r'$h[n]$ 波形')
plt.xlabel('n')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

# 计算并绘制 h[n] 的幅度谱
h_n_fft = np.fft.fft(h_n)
frequencies = np.fft.fftfreq(N)

# 子图2：幅度谱
plt.subplot(3, 1, 2)
plt.plot(frequencies[:N//2], np.abs(h_n_fft)[:N//2], label='Magnitude Spectrum')
plt.title(r'$h[n]$ 幅度谱')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.legend()

# 子图3：分贝表示形式
plt.subplot(3, 1, 3)
plt.plot(frequencies[:N//2], 20 * np.log10(np.abs(h_n_fft)[:N//2] + 1e-10), label='Magnitude Spectrum (dB)')
plt.title(r'$h[n]$ 分贝表示')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()

# 显示所有子图
plt.tight_layout()
plt.show()
