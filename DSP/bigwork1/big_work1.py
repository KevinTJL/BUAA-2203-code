import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fft
import scipy.io.wavfile as wav

# import matplotlib
# print(matplotlib.__version__)

# 读取音频文件
file_path = "./DSP/bigwork1/PRJ01.wav"  # 请确保该文件在同一目录下
fs, x = wav.read(file_path)
n = np.arange(len(x))
t = n / fs  # 计算连续时间

# 绘制离散信号 x[n] 和连续信号 x(t)
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.stem(n[:100], x[:100], markerfmt='ro', linefmt='b-', basefmt='k-')
plt.xlabel("n")
plt.ylabel("x[n]")
plt.title("离散时间信号 x[n]")

plt.subplot(2, 1, 2)
plt.plot(t[:100], x[:100])
plt.xlabel("t (秒)")
plt.ylabel("x(t)")
plt.title("连续时间信号 x(t)")
plt.tight_layout()
plt.show()

# 计算数字频谱
w, X_w = signal.freqz(x, worN=1024)
X_w_magnitude = np.abs(X_w)
X_w_dB = 20 * np.log10(X_w_magnitude + 1e-6)  # 避免 log(0)

# 绘制 |X(e^jω)| 及其 dB 形式
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.plot(w / np.pi, X_w_magnitude)
plt.xlabel("Normalized Frequency (π rad/sample)")
plt.ylabel("|X(e^jω)|")
plt.title("数字频谱幅度")

plt.subplot(2, 1, 2)
plt.plot(w / np.pi, X_w_dB)
plt.xlabel("Normalized Frequency (π rad/sample)")
plt.ylabel("20lg|X(e^jω)|")
plt.title("数字频谱 (dB scale)")
plt.tight_layout()
plt.show()

# 计算模拟频谱
N = len(x)
freqs = np.fft.fftfreq(N, d=1/fs)  # 计算频率轴
X_f = fft.fft(x)
X_f_magnitude = np.abs(X_f)
X_f_dB = 20 * np.log10(X_f_magnitude + 1e-6)  # 避免 log(0)

# 绘制 |X_c(f)| 及其 dB 形式
plt.figure(figsize=(12, 5))
plt.subplot(2, 1, 1)
plt.plot(freqs[:N // 2], X_f_magnitude[:N // 2])
plt.xlabel("Frequency (Hz)")
plt.ylabel("|X_c(f)|")
plt.title("模拟频谱幅度")

plt.subplot(2, 1, 2)
plt.plot(freqs[:N // 2], X_f_dB[:N // 2])
plt.xlabel("Frequency (Hz)")
plt.ylabel("20lg|X_c(f)|")
plt.title("模拟频谱 (dB scale)")
plt.tight_layout()
plt.show()
