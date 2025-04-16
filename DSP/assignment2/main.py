import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 第一步：线性卷积函数实现
def linear_convolution(x, h):
    """
    计算输入信号 x 和单位脉冲响应 h 的线性卷积
    """
    N = len(x) + len(h) - 1  # 计算卷积后的序列长度
    y = np.zeros(N)
    for n in range(N):
        for k in range(len(h)):
            if n - k >= 0 and n - k < len(x):
                y[n] += x[n - k] * h[k]
    return y

# 第二步：圆周卷积基于DFT计算
def circular_convolution(x, h):
    """
    计算输入信号 x 和单位脉冲响应 h 的圆周卷积，基于DFT
    """
    N = len(x)
    X = np.fft.fft(x, N)  # 计算x的DFT
    H = np.fft.fft(h, N)  # 计算h的DFT
    Y = X * H  # 进行频域相乘（圆周卷积）
    y = np.fft.ifft(Y)  # 将结果转换回时域
    return np.real(y)  # 返回实数部分

# 测试数据：假设输入序列 x 和单位脉冲响应 h
M = 25  # R_M[n] 的长度
N = 15  # R_N[n] 的长度
n_M = np.arange(M)  # 用于 R_M[n]
n_N = np.arange(N)  # 用于 R_N[n]

# 生成 R_M[n] 和 R_N[n]，假设是单位脉冲序列
R_M = np.zeros(M)
R_M[0] = 1  # 单位脉冲信号
R_N = np.zeros(N)
R_N[0] = 1  # 单位脉冲信号

# 计算 h[n] = 0.9^n * R_M[n]
h = 0.9 ** n_M * R_M
x = R_N

# 计算线性卷积
y_linear = linear_convolution(x, h)

# 计算圆周卷积
y_circular = circular_convolution(x, h)

# 绘制结果
plt.figure(figsize=(12, 8))

# 子图1：输入序列 x 和单位脉冲响应 h
plt.subplot(3, 1, 1)
plt.stem(x, label='Input sequence x[n]', basefmt=" ")
plt.stem(h, label='Impulse response h[n]', basefmt=" ")
plt.title("Input and Impulse Response")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# 子图2：线性卷积结果
plt.subplot(3, 1, 2)
plt.stem(np.arange(len(y_linear)), y_linear, label='Linear Convolution y[n]', basefmt=" ")
plt.title("Linear Convolution Result")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# 子图3：圆周卷积结果
plt.subplot(3, 1, 3)
plt.stem(np.arange(len(y_circular)), y_circular, label='Circular Convolution y[n]', basefmt=" ")
plt.title("Circular Convolution Result (DFT)")
plt.xlabel("n")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

