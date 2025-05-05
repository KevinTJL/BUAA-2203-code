import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 系统函数分子与分母系数（按 z 的降幂排列）
b = [1, -3/4]                 # 对应分子: 1 - 3/4 z^(-1)
a = [1, 7/6, 1/3]             # 对应分母: 1 + 7/6 z^(-1) + 1/3 z^(-2)

# 计算频率响应
w, h = freqz(b, a, worN=1024)

# 绘制幅度响应
plt.figure(figsize=(10, 4))
plt.plot(w / np.pi, np.abs(h))
plt.title("系统幅度响应 |H(e^{jω})|")
plt.xlabel("归一化频率 (×π rad/sample)")
plt.ylabel("幅度")
plt.grid(True)
plt.tight_layout()
plt.show()
