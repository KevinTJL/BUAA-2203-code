import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import freqz, buttord, butter, group_delay
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或 'SimHei'，视具体环境而定
# ———— 1. 读取信号 & 构造时间轴 ————
fs =   3600    # 采样频率 (Hz)
T  =   60    # 总采样时长 (秒)
data = np.loadtxt('PRJ03.txt')
N    = len(data)
n    = np.arange(N)
t    = n / fs

# 绘图：离散下标 vs 实际时间
plt.figure(figsize=(12,4))
plt.stem(n, data, basefmt=' ')
plt.title('ECG 波形（离散下标 n）')
plt.xlabel('样本下标 n')
plt.ylabel('幅值')
plt.show()

plt.figure(figsize=(12,4))
plt.plot(t, data)
plt.title('ECG 波形（实际时间 t）')
plt.xlabel('时间 (s)')
plt.ylabel('幅值')
plt.show()


# ———— 2. DFT & DTFT 分析 ————
X = np.fft.fft(data)
freqs = np.fft.fftfreq(N, d=1/fs)
# 只取正频率部分
pos = freqs >= 0

plt.figure(figsize=(12,4))
plt.plot(freqs[pos], np.abs(X)[pos])
plt.title('DFT 幅度谱')
plt.xlabel('频率 (Hz)')
plt.ylabel('|X[k]|')
plt.show()

plt.figure(figsize=(12,4))
plt.plot(freqs[pos], 20*np.log10(np.abs(X)[pos]))
plt.title('DFT 幅度谱（dB）')
plt.xlabel('频率 (Hz)')
plt.ylabel('20 log10 |X[k]|')
plt.show()

# DTFT via freqz
w, H = freqz(data, worN=1024)
f = w*fs/(2*np.pi)
plt.figure(figsize=(12,4))
plt.plot(f, np.abs(H))
plt.title('DTFT 幅度谱')
plt.xlabel('频率 (Hz)')
plt.ylabel('|H(e^{jω})|')
plt.show()

plt.figure(figsize=(12,4))
plt.plot(f, 20*np.log10(np.abs(H)))
plt.title('DTFT 幅度谱（dB）')
plt.xlabel('频率 (Hz)')
plt.ylabel('20 log10 |H(e^{jω})|')
plt.show()


# ———— 3. IIR 滤波器设计 ————
# 规格参数（Hz）

import numpy as np
from scipy.signal import buttord, butter, freqz
import matplotlib.pyplot as plt

# 1) 规范化数字频率
Wp = 0.2   # = 0.2π
Ws = 0.3   # = 0.3π

# 2) 振幅规范转换到 dB
delta_p = 1/100
delta_s = 1/1000
gpass = -20 * np.log10(1 - delta_p)  # 通带最大衰减 dB
gstop = -20 * np.log10(delta_s)      # 阻带最小衰减 dB

# 3) 计算最小阶数和截止频率
N, Wn = buttord(Wp, Ws, gpass, gstop)

# 4) 设计低通 Butterworth 数字滤波器
b, a = butter(N, Wn, btype='low', analog=False)

# 5) 验证——绘制幅度 & 相位响应
w, h = freqz(b, a, worN=1024)
f = w / np.pi  # 归一化到 π

# 频率响应
w2, h2 = freqz(b, a, worN=1024)
f2 = w2*fs/(2*np.pi)
plt.figure(figsize=(12,4))
plt.plot(f2, np.abs(h2))
plt.title('IIR 幅频响应')
plt.xlabel('频率 (Hz)')
plt.ylabel('|H(e^{jω})|')
plt.show()

plt.figure(figsize=(12,4))
plt.plot(f2, 20*np.log10(np.abs(h2)))
plt.title('IIR 幅频响应（dB）')
plt.xlabel('频率 (Hz)')
plt.ylabel('20 log10 |H|')
plt.show()

plt.figure(figsize=(12,4))
plt.plot(f2, np.angle(h2))
plt.title('IIR 相频响应')
plt.xlabel('频率 (Hz)')
plt.ylabel('相位 (rad)')
plt.show()

w_g, gd = group_delay((b, a), w=1024)
f_g = w_g*fs/(2*np.pi)
plt.figure(figsize=(12,4))
plt.plot(f_g, gd)
plt.title('IIR 群时延')
plt.xlabel('频率 (Hz)')
plt.ylabel('时延 (样本点)')
plt.show()


# ———— 4. 频域滤波 & IDFT ————
# 将 DFT 乘以 IIR 频率响应（或理想低通窗）
H_interp = np.interp(freqs, f2, np.abs(h2), left=0, right=0)
X_filt = X * H_interp
x_rec  = np.fft.ifft(X_filt)

plt.figure(figsize=(12,4))
plt.plot(t, data, label='原始')
plt.plot(t, x_rec.real, label='滤波后', alpha=0.8)
plt.title('时域对比')
plt.xlabel('时间 (s)')
plt.ylabel('幅值')
plt.legend()
plt.show()

import matplotlib.pyplot as plt

# 假设 freqs[pos], X, X_filt 都已经算好了
plt.figure(figsize=(12,4))

# 左边子图：原始幅度谱
plt.subplot(1, 2, 1)              # 1 行 2 列，第 1 个子图
plt.plot(freqs[pos], np.abs(X)[pos])
plt.title('原始幅度谱')
plt.xlabel('频率 (Hz)')
plt.ylabel('|X|')

# 右边子图：滤波后幅度谱
plt.subplot(1, 2, 2)              # 1 行 2 列，第 2 个子图
plt.plot(freqs[pos], np.abs(X_filt)[pos], alpha=0.8)
plt.title('滤波后幅度谱')
plt.xlabel('频率 (Hz)')
plt.ylabel('|X|')

plt.tight_layout()                # 自动调整子图间距
plt.show()


plt.figure(figsize=(12,4))
plt.plot(freqs[pos], 20*np.log10(np.abs(X)[pos]), label='原始')
plt.plot(freqs[pos], 20*np.log10(np.abs(X_filt)[pos]), label='滤波后', alpha=0.8)
plt.title('幅度谱对比（dB）')
plt.xlabel('频率 (Hz)')
plt.ylabel('20 log10 |X|')
plt.legend()
plt.show()
