import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或 'SimHei'，视具体环境而定
plt.rcParams['axes.unicode_minus'] = False  # 确保负号显示正确

# 参数定义
M = 25  # x[n]的长度
N = 15  # R_M[n]的长度
n = np.arange(0, M)  # n的范围
R_M = np.ones(N)  # 定义R_M[n]为全1序列
h = 0.9 ** n * np.pad(R_M, (0, M - N), 'constant')  # h[n] = 0.9^n * R_M[n]，并补充长度

# 生成输入序列x[n]（假设为R_M[n]）
x = np.pad(R_M, (0, M - N), 'constant')  # 补充长度，确保x和h长度一致

# 计算卷积
y1 = np.convolve(x, h, 'full')  # 全卷积
y2 = np.convolve(x, h, 'same')  # 相同长度卷积

# 绘制输入序列、h[n]、y1[n]和y2[n]
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.stem(n, x[:len(n)], basefmt=" ")
plt.title("输入序列 x[n]")
plt.subplot(2, 2, 2)
plt.stem(n, h[:len(n)], basefmt=" ")
plt.title("单位脉冲响应 h[n]")
plt.subplot(2, 2, 3)
plt.stem(np.arange(len(y1)), y1, basefmt=" ")
plt.title("卷积输出 y1[n]")
plt.subplot(2, 2, 4)
plt.stem(np.arange(len(y2)), y2, basefmt=" ")
plt.title("卷积输出 y2[n]")
plt.tight_layout()
plt.show()

# DFT计算
L = M + N - 1  # DFT点数
Y1_dft = np.fft.fft(y1, L)
Y2_dft = np.fft.fft(y2, L)

# 绘制DFT幅度谱
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(np.abs(Y1_dft))
plt.title("y1[n] 的DFT幅度谱")
plt.subplot(2, 1, 2)
plt.plot(np.abs(Y2_dft))
plt.title("y2[n] 的DFT幅度谱")
plt.tight_layout()
plt.show()

# 圆周卷积（使用FFT和IFFT）
L = 2 * max(M, N)  # 为圆周卷积选择合适的长度，通常是信号长度的最大值的两倍
X = np.fft.fft(x, L)
H = np.fft.fft(h, L)
Y = np.fft.ifft(X * H)  # 在频域相乘并逆变换得到卷积结果

# 绘制输入序列、h[n]、y[n]
plt.figure(figsize=(12, 8))

# # 绘制输入序列x[n]
# plt.subplot(2, 2, 1)
# plt.stem(n, x[:len(n)], basefmt=" ")
# plt.title("输入序列 x[n]")

# # 绘制单位脉冲响应h[n]
# plt.subplot(2, 2, 2)
# plt.stem(n, h[:len(n)], basefmt=" ")
# plt.title("单位脉冲响应 h[n]")

# 绘制圆周卷积输出 y[n]
plt.stem(np.arange(L), np.abs(Y), basefmt=" ")
plt.title("圆周卷积输出 y[n]")

plt.tight_layout()
plt.show()

# DFT计算
Y_dft = np.fft.fft(Y, L)  # 计算y[n]的DFT

# 绘制DFT幅度谱
plt.figure(figsize=(12, 8))

# 绘制y[n]的DFT幅度谱
plt.subplot(2, 1, 1)
plt.plot(np.abs(Y_dft), label='|Y[k]|', color='b')
plt.title("y[n] 的DFT幅度谱")
plt.xlabel("频率点 k")
plt.ylabel("幅度")
plt.legend()

plt.tight_layout()
plt.show()
