import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 系统函数的系数
b = [0, 0.5]           # 分子系数，对应 0.5*z^(-1)
a = [1, 2/3]           # 分母系数，对应 1 + (2/3)*z^(-1)

# 计算频率响应
w, h = freqz(b, a, worN=8000)

# 绘制幅度响应
plt.figure(figsize=(8, 4))
plt.plot(w / np.pi, np.abs(h))  # 归一化频率（单位π）
plt.title('幅度响应 |H(e^{jω})|')
plt.xlabel('归一化频率 (×π rad/sample)')
plt.ylabel('幅度')
plt.grid(True)
plt.tight_layout()
plt.show()
