import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import soundfile as sf

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 如果需要在 Jupyter Notebook 中直接播放音频，可以使用:
# from IPython.display import Audio

# 1. 读取音频文件
# -------------------------------------------------
# 这里假设音频文件 PRJ01.wav 与脚本位于同一路径下
x, fs = sf.read('./DSP/assignment1/PRJ01.wav')  # x 为音频信号, fs 为采样率

# 如果是多通道音频, 可以先取一个声道进行分析:
if x.ndim > 1:
    x = x[:, 0]  # 仅取左声道作为示例

# 2. 播放音频 (根据需求和环境决定是否需要)
# -------------------------------------------------
# 在部分 Python 环境下可以这样播放音频(如 Jupyter Notebook):
# Audio(data=x, rate=fs)
# 或者使用其他第三方库，如 pyaudio 等

# 3. 画时域波形
# -------------------------------------------------
n = np.arange(len(x))       # 离散时间索引 n
t = n / fs                  # 连续时间 t (秒)

plt.figure(figsize=(8, 4))
plt.plot(n, x)
plt.title('音频序列 x[n]')
plt.xlabel('n')
plt.ylabel('幅度')
plt.grid(True)
plt.tight_layout()

plt.figure(figsize=(8, 4))
plt.plot(t, x)
plt.title('原始波形 x_c(t)')
plt.xlabel('时间 (秒)')
plt.ylabel('幅度')
plt.grid(True)
plt.tight_layout()

# 4. 计算并绘制数字频谱
# -------------------------------------------------
# (1) 计算 FFT
N = 2 ** int(np.ceil(np.log2(len(x))))  # 取大于等于 len(x) 的最近 2 的整数次幂
X = np.fft.fft(x, N)                    # 计算 FFT
X_mag = np.abs(X[:N // 2])              # 只取正频部分的幅度
w = np.linspace(0, np.pi, N // 2)       # 归一化角频率 [0, π]

# (2) 幅度谱 |X(e^{jω})|
plt.figure(figsize=(8, 4))
plt.plot(w, X_mag)
plt.title('幅度谱 |X(e^{jω})|')
plt.xlabel('归一化角频率 ω')
plt.ylabel('幅度')
plt.grid(True)
plt.tight_layout()

# (3) 分贝尺度 20lg|X(e^{jω})|
plt.figure(figsize=(8, 4))
# 避免出现 0 幅度时 log10 出现警告，可加一个很小的常数
plt.plot(w, 20 * np.log10(X_mag + 1e-12))
plt.title('分贝尺度 20lg|X(e^{jω})|')
plt.xlabel('归一化角频率 ω')
plt.ylabel('幅度 (dB)')
plt.grid(True)
plt.tight_layout()

# 5. 将数字频谱转换为模拟频率并绘制
# -------------------------------------------------
f = w / (2 * np.pi) * fs    # 从归一化角频率转换到实际频率
Xc_mag = X_mag              # 与 X_mag 相同，这里仅做区分以示概念

# (1) 模拟频谱 |X_c(if)|
plt.figure(figsize=(8, 4))
plt.plot(f, Xc_mag)
plt.title('模拟频谱 |X_c(if)|')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.grid(True)
plt.tight_layout()

# (2) 分贝尺度 20lg|X_c(if)|
plt.figure(figsize=(8, 4))
plt.plot(f, 20 * np.log10(Xc_mag + 1e-12))
plt.title('分贝尺度 20lg|X_c(if)|')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度 (dB)')
plt.grid(True)
plt.tight_layout()

plt.show()