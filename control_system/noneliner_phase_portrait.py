import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 非线性函数 f(c)
def f(c):
    if c < -1:
        return -2
    elif c > 1:
        return 2
    else:
        return 0

# 定义微分方程组
def system(t, y):
    c, v = y
    return [v, f(c) - c]

# 时间范围和初值
t = np.linspace(0, 20, 1000)
y0 = [1.5, 0.0]  # 初始值 c(0)=1.5, c'(0)=0

# 数值解
sol = solve_ivp(system, [t[0], t[-1]], y0, t_eval=t)

# 绘图
plt.figure(figsize=(6, 6))
plt.plot(sol.y[0], sol.y[1], label='Trajectory')
plt.axvline(1, color='r', linestyle='--', label='c = ±1 boundary')
plt.axvline(-1, color='r', linestyle='--')
plt.xlabel('c')
plt.ylabel('c\'')
plt.title('Phase Portrait of the Nonlinear System')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()
