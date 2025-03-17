import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# x = 5
# 定义传递函数 H(s) = 10 / (s^2 + 2s + 10)
numerator = [4, 10]          # 分子系数
denominator = [1,2,1,0]  # 分母系数
system = signal.TransferFunction(numerator, denominator)

# 生成频率范围（对称以涵盖正负频率）
frequencies = np.logspace(-2, 2, 500)  # 从 0.01 rad/s 到 100 rad/s
# frequencies = np.concatenate((-frequencies[::-1], frequencies))  # 包含负频率

# 计算频率响应
w, h = signal.freqresp(system, w=frequencies)

# 绘制奈奎斯特图
plt.figure(figsize=(8, 8))
plt.plot(h.real, h.imag, label="Positive Frequency")   # 正频率部分
plt.plot(h.real, -h.imag, label="Negative Frequency")  # 负频率部分
plt.plot([-1], [0], 'ro')  # 标记 -1 点

# 设置图形属性
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.xlabel("Real")
plt.ylabel("Imaginary")
plt.title("Nyquist Plot")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
