import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 设定频率范围
omega = np.linspace(0, np.pi, 1000)

# 技术指标
W1 = 0.2 * np.pi   # 第一截止频率 0-0.2π
W2 = 0.3 * np.pi   # 第二截止频率 0.3π-π
A1 = 0.89125
A2 = 0.17783

# 巴特沃斯滤波器设计
# 计算最小阶数 N 和截止频率
Wp = W1 / np.pi   # 正规化的通带截止频率
Ws = W2 / np.pi   # 正规化的阻带截止频率
Rp = -20 * np.log10(A1)  # 通带衰减
Rs = -20 * np.log10(A2)  # 阻带衰减

# 使用butter函数计算巴特沃斯滤波器
N, Wn = butter(4, [Wp, Ws], btype='band', analog=False, output='ba')  # 设计带通滤波器

# 计算频率响应
w, h = freqz(N, Wn, worN=omega)

# 绘制幅度响应
plt.figure(figsize=(10, 6))
plt.plot(w / np.pi, np.abs(h), label='滤波器幅度响应 $|H(e^{j\omega})|$')
plt.title('数字滤波器的幅度响应')
plt.xlabel('频率 (单位: $\pi$ rad/sample)')
plt.ylabel('幅度')
plt.grid(True)
plt.legend()
plt.show()
