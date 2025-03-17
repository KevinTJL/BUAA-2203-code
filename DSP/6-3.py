import numpy as np
import matplotlib.pyplot as plt

# 给定的连续时间信号
def x_c1(t):
    return np.cos(2 * np.pi * t)

def x_c2(t):
    return np.cos(6 * np.pi * t)

def x_c3(t):
    return np.cos(10 * np.pi * t)

# 采样频率
Omega_s = 8 * np.pi  # 采样角频率 rad/s
T = 2 * np.pi / Omega_s  # 采样周期 T = 1 / F_s

# 定义连续时间范围
t_cont = np.linspace(0, 2, 1000)  # 0 到 2 秒，1000 个点

# 计算连续信号
x1_cont = x_c1(t_cont)
x2_cont = x_c2(t_cont)
x3_cont = x_c3(t_cont)

# 采样点
n = np.arange(0, 2, T)  # 采样时刻
x1_sampled = x_c1(n)
x2_sampled = x_c2(n)
x3_sampled = x_c3(n)

# 绘制连续信号和采样点
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

# 绘制 x1(t) 和采样点
axes[0].plot(t_cont, x1_cont, label="Continuous x1(t)", color='orange')
axes[0].stem(n, x1_sampled, linefmt='r-', markerfmt='ro', basefmt=" ", label="Sampled x1[n]")
axes[0].set_title("Signal x1(t) and its samples")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")
axes[0].legend()
axes[0].grid()

# 绘制 x2(t) 和采样点
axes[1].plot(t_cont, x2_cont, label="Continuous x2(t)", color='orange')
axes[1].stem(n, x2_sampled, linefmt='r-', markerfmt='ro', basefmt=" ", label="Sampled x2[n]")
axes[1].set_title("Signal x2(t) and its samples")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Amplitude")
axes[1].legend()
axes[1].grid()

# 绘制 x3(t) 和采样点
axes[2].plot(t_cont, x3_cont, label="Continuous x3(t)", color='orange')
axes[2].stem(n, x3_sampled, linefmt='r-', markerfmt='ro', basefmt=" ", label="Sampled x3[n]")
axes[2].set_title("Signal x3(t) and its samples")
axes[2].set_xlabel("Time (s)")
axes[2].set_ylabel("Amplitude")
axes[2].legend()
axes[2].grid()

plt.tight_layout()
plt.show()