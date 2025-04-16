import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import kaiser
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 参数定义
N = 100  # 假设长度为100，可以根据需要调整
n = np.arange(N)
A = 46  # Kaiser窗的A值
beta = 4.09  # Kaiser窗的beta值

# 计算hd[n]
hd_n = np.sinc(0.45 * (n - 27) / np.pi)

# 计算Kaiser窗w[n]
w_n = kaiser(N, beta)

# 计算h[n] = hd[n] * w[n]
h_n = hd_n * w_n

# 计算h[n]的频率响应
H_n_fft = np.fft.fft(h_n, N)
frequencies = np.fft.fftfreq(N)

# 计算幅度响应
H_magnitude = np.abs(H_n_fft)

# 计算分贝响应 20 * log10(|H(e^jw)|)
H_dB = 20 * np.log10(H_magnitude + 1e-10)  # 避免log(0)

# 绘制结果
plt.figure(figsize=(12, 8))

# 子图1：h[n]时域波形
plt.subplot(3, 1, 1)
plt.stem(n, h_n, label=r'$h[n] = hd[n] \cdot w[n]$', basefmt=" ")
plt.title(r'$h[n]$ 时域波形')
plt.xlabel('n')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()

# 子图2：h[n]的幅度响应
plt.subplot(3, 1, 2)
plt.plot(frequencies[:N//2], H_magnitude[:N//2], label=r'$|H(e^{j\omega})|$')
plt.title(r'$h[n]$ 的幅度响应')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid()

# 子图3：h[n]的分贝响应
plt.subplot(3, 1, 3)
plt.plot(frequencies[:N//2], H_dB[:N//2], label=r'$20\log_{10}(|H(e^{j\omega})|)$')
plt.title(r'$h[n]$ 的分贝响应')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend()
plt.grid()

# 显示所有子图
plt.tight_layout()
plt.show()
