import numpy as np
import matplotlib.pyplot as plt

# 给定序列长度
N = 16

# 假设 x[n] 是单位阶跃序列 R_N[n]
# 因为没有明确给出序列 x[n] 的值，假设 R_N[n] 是一个常见的序列，如单位阶跃序列
x_n = np.ones(N)  # 对于单位阶跃序列，所有 x[n] = 1

# 计算频率响应 X(e^jω)
omega = np.linspace(-np.pi, np.pi, 400)  # 频率范围
X_omega = np.zeros(len(omega), dtype=complex)

for i, w in enumerate(omega):
    X_omega[i] = np.sum(x_n * np.exp(-1j * w * np.arange(N)))

# 绘制幅度响应 |X(e^jω)|
plt.plot(omega, np.abs(X_omega))
plt.title("Magnitude Response of X(e^jω)")
plt.xlabel("Frequency (ω)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.show()
