import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 参数设置
Fs = 500          # 采样率 (Hz)
T = 1.0           # 信号时长 (秒)
t = np.linspace(0, T, int(Fs*T), endpoint=False)

# 构造一个复合信号（带相位）
x = np.sin(2*np.pi*10*t + np.pi/3) + 0.5*np.sin(2*np.pi*50*t - np.pi/4)

# 傅里叶变换
X = fft(x)
freqs = fftfreq(len(t), 1/Fs)

# 取正频率部分
half = len(t) // 2
X_mag = 2.0 / len(t) * np.abs(X[:half])  # 幅度
X_phase = np.angle(X[:half])            # 相位（弧度）

# 绘图
plt.figure(figsize=(12, 6))

# 幅度谱
plt.subplot(2, 1, 1)
plt.stem(freqs[:half], X_mag)
plt.title("幅度谱")
plt.xlabel("频率 (Hz)")
plt.ylabel("幅度")

# 相位谱
plt.subplot(2, 1, 2)
plt.stem(freqs[:half], X_phase)
plt.title("相位谱")
plt.xlabel("频率 (Hz)")
plt.ylabel("相位 (radians)")
plt.tight_layout()
plt.show()
