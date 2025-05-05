import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 饱和函数 sat(x)
def sat(x):
    if x > 2:
        return 2
    elif x < -2:
        return -2
    else:
        return x

# 状态空间模型
def system(t, y):
    c, c_dot = y
    e = -c
    u = sat(e)
    return [c_dot, u - c_dot]

# 初始条件和时间设置
y0 = [-3, 0]
t_eval = np.linspace(0, 30, 1000)
sol = solve_ivp(system, [t_eval[0], t_eval[-1]], y0, t_eval=t_eval)

# Phase trajectory: (c, c')
plt.figure(figsize=(6, 5))
plt.plot(sol.y[0], sol.y[1])
plt.axvline(-2, color='r', linestyle='--', label='Saturation limits')
plt.axvline(2, color='r', linestyle='--')
plt.axhline(0, color='k', linewidth=0.5)
plt.xlabel('c')
plt.ylabel("c'")
plt.title('Phase Trajectory')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()

# Response curve c(t)
plt.figure(figsize=(8, 4))
plt.plot(sol.t, sol.y[0])
plt.xlabel('Time t')
plt.ylabel('c(t)')
plt.title('Response Curve')
plt.grid(True)
plt.show()
