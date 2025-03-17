import numpy as np
import matplotlib.pyplot as plt

# 计算卷积
def compute_convolution(h, x):
    return np.convolve(h, x)

# 设置样本范围
N_h1, N_x1 = 5, 7  # R4[n] 和 R6[n] 的长度
N_h2, N_x2 = 5, 1  # (1/2)^n R4[n] 和 δ[n-2] 的长度
n_h1 = np.arange(N_h1)
n_x1 = np.arange(N_x1)
n_h2 = np.arange(N_h2)
n_x2 = np.array([2])

# (1) h[n] = R4[n], x[n] = R6[n]
h1 = np.arange(N_h1)  # R4[n] = [0, 1, 2, 3, 4]
x1 = np.arange(N_x1)  # R6[n] = [0, 1, 2, 3, 4, 5, 6]
y1 = compute_convolution(h1, x1)

# (2) h[n] = (1/2)^n R4[n], x[n] = δ[n-2]
h2 = (1/2) ** n_h2 * np.arange(N_h2)
x2 = np.array([1])  # δ[n-2] 仅在 n=2 处为 1
y2 = compute_convolution(h2, x2)

# 画图
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.stem(np.arange(len(y1)), y1, basefmt="C0:")
plt.title("Convolution: $h[n]=R_4[n]$, $x[n]=R_6[n]$")
plt.xlabel("n")
plt.ylabel("y[n]")
plt.grid()

plt.subplot(1,2,2)
plt.stem(np.arange(len(y2)), y2, basefmt="C0:")
plt.title("Convolution: $h[n]=(1/2)^n R_4[n]$, $x[n]=\delta[n-2]$")
plt.xlabel("n")
plt.ylabel("y[n]")
plt.grid()

plt.tight_layout()
plt.show()
