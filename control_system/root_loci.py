import numpy as np
import matplotlib.pyplot as plt
from control import tf, rlocus

# 定义开环传递函数 G(s)
K = 1  # 设置初始增益 K 值
numerator = [-1*K, 2*K]  # 分子 K*(s + 10)
denominator = [1,3,-4]  # 分母 s(s + 1)(s + 4)^2

# 创建传递函数
system = tf(numerator, denominator)

# 绘制根轨迹
plt.figure(figsize=(8, 6))
rlocus(system)
plt.title('Root Locus of the System')
plt.grid(True)
plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.signal as signal

# # 定义传递函数 G(s) 的组成部分
# T_values = np.linspace(0.01, 1, 100)  # T 从较小的值变化到 10

# # 创建用于存储不同 T 值下的极点位置的列表
# real_parts = []
# imag_parts = []

# # 为不同的 T 值生成极点位置
# for T in T_values:
#     num = [2.6]  # 分子 (常数 2.6)
#     den = [0.1 * T, (1 + 0.1 * T), 10, 0]  # 分母 s(0.1s+1)(Ts+1)
#     system = signal.TransferFunction(num, den)
#     poles = np.roots(den)
#     real_parts.append(poles.real)
#     imag_parts.append(poles.imag)

# # 绘制根轨迹
# plt.figure(figsize=(8, 6))
# for i in range(len(T_values)):
#     plt.scatter(real_parts[i], imag_parts[i], color='blue', marker='x')

# plt.title('G(s) 的根轨迹图，T 从 0 变化到 ∞')
# plt.xlabel('实轴')
# plt.ylabel('虚轴')
# plt.axhline(0, color='black',linewidth=0.5)
# plt.axvline(0, color='black',linewidth=0.5)
# plt.grid(True)
# plt.show()

