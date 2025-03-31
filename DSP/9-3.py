import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ========== 参数设置 ==========
N = 5  # 可以根据题目需要修改

# ========== 1. 系统函数 H(z) = 1 - z^{-N} ==========
# 对应于差分方程 y[n] = x[n] - x[n - N]
# 在 z 域下, 系统函数 H(z) = 1 - z^(-N)
# 若用滤波器系数表示(b/a), 则:
# b = [1, 0, 0, ..., 0, -1] (长度 N+1, 其中 b[0] = 1, b[N] = -1)
# a = [1]
b = np.zeros(N + 1)
b[0] = 1
b[-1] = -1  # 或者 b[N] = -1
a = [1]

# ========== 2. 画极零点图 (Pole-Zero Plot) ==========
# 求零点和极点
zeros = np.roots(b)
poles = np.roots(a)

plt.figure(figsize=(6, 6))
plt.axhline(0, color='0.7')  # x轴
plt.axvline(0, color='0.7')  # y轴

# 画零点(用 'o')和极点(用 'x')
plt.plot(zeros.real, zeros.imag, 'o', label='Zeros')
plt.plot(poles.real, poles.imag, 'x', label='Poles')

# 画单位圆
theta = np.linspace(0, 2*np.pi, 200)
unit_circle = np.exp(1j*theta)
plt.plot(unit_circle.real, unit_circle.imag, '--', color='gray', label='Unit Circle')

plt.title('Pole-Zero Plot')
plt.xlabel('Real Part')
plt.ylabel('Imag Part')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()

# ========== 3. 画单位冲激响应 (Impulse Response) ==========
# 构造一个单位冲激序列，长度取 2N+1 以方便观察
imp_len = 2*N + 1
impulse = np.zeros(imp_len)
impulse[0] = 1  # delta[n]

# 通过 lfilter 计算系统对冲激输入的响应
h = signal.lfilter(b, a, impulse)

plt.figure()
plt.stem(range(imp_len), h)
plt.title('Impulse Response')
plt.xlabel('n')
plt.ylabel('h[n]')
plt.grid(True)
plt.show()

# ========== 4. 画频率响应 (Frequency Response) ==========
w, H = signal.freqz(b, a, worN=512)  # w 是数字角频率，H 是频率响应(复数)

plt.figure(figsize=(10, 4))

# (a) 幅度响应
plt.subplot(1, 2, 1)
plt.plot(w, np.abs(H))
plt.title('Magnitude Response')
plt.xlabel('Frequency (rad/sample)')
plt.ylabel('|H(e^{jω})|')
plt.grid(True)

# (b) 相位响应
plt.subplot(1, 2, 2)
plt.plot(w, np.angle(H))
plt.title('Phase Response')
plt.xlabel('Frequency (rad/sample)')
plt.ylabel('∠H(e^{jω}) (radians)')
plt.grid(True)

plt.tight_layout()
plt.show()