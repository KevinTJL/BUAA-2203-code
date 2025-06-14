#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

# 参数
dt = 0.01            # 采样周期（秒）
N  = 60000           # 样本数量

# 1. 读取 ins_c.txt 中的初始姿态（偏航Ψ、俯仰θ、横滚φ），列索引分别是 10,11,12
data_ins = np.loadtxt('ins_c.txt')
yaw0, pitch0, roll0 = np.deg2rad(data_ins[0, 10]), \
                      np.deg2rad(data_ins[0, 11]), \
                      np.deg2rad(data_ins[0, 12])

# 2. 欧拉角 3-1-2 转四元数
def euler312_to_quat(psi, phi, theta):
    c1, s1 = np.cos(psi/2), np.sin(psi/2)
    c2, s2 = np.cos(phi/2), np.sin(phi/2)
    c3, s3 = np.cos(theta/2), np.sin(theta/2)
    q0 = c1*c2*c3 + s1*s2*s3
    q1 = s1*c2*c3 - c1*s2*s3
    q2 = c1*s2*c3 + s1*c2*s3
    q3 = c1*c2*s3 - s1*s2*c3
    return np.array([q0, q1, q2, q3])

q0 = euler312_to_quat(yaw0, roll0, pitch0)

# 3. 读取角速度 p, q_, r
mat = loadmat('WNBB.mat')
p   = mat['p'].flatten()
q_  = mat['q'].flatten()   # 用 q_ 避免变量名冲突
r   = mat['r'].flatten()

# 四元数导数函数
def quat_derivative(q, p, qv, r):
    Omega = np.array([
        [  0, -p,  -qv, -r],
        [  p,  0,    r, -qv],
        [ qv, -r,    0,   p],
        [  r,  qv,  -p,   0]
    ])
    return 0.5 * Omega.dot(q)

# 4. 数值积分：Euler 与 RK4
def integrate(method='rk4'):
    Q = np.zeros((N, 4))
    Q[0] = q0
    for k in range(N-1):
        omega = (p[k], q_[k], r[k])
        qc = Q[k]
        if method == 'euler':
            dq = quat_derivative(qc, *omega)
            qn = qc + dt * dq
        else:  # RK4
            k1 = quat_derivative(qc, *omega)
            k2 = quat_derivative(qc + dt/2*k1, *omega)
            k3 = quat_derivative(qc + dt/2*k2, *omega)
            k4 = quat_derivative(qc + dt*k3, *omega)
            qn = qc + dt*(k1 + 2*k2 + 2*k3 + k4)/6
        Q[k+1] = qn / np.linalg.norm(qn)
    return Q

Q_euler = integrate('euler')
Q_rk4   = integrate('rk4')

# 5. 四元数 转 欧拉角 3-1-2
def quat_to_euler312(Q):
    q0, q1, q2, q3 = Q[:,0], Q[:,1], Q[:,2], Q[:,3]
    phi   = np.arctan2(2*(q0*q1 + q2*q3),
                       q0**2 - q1**2 - q2**2 + q3**2)
    theta = np.arcsin(2*(q0*q2 - q1*q3))
    psi   = np.arctan2(2*(q0*q3 + q1*q2),
                       q0**2 + q1**2 - q2**2 - q3**2)
    return np.rad2deg(phi), np.rad2deg(theta), np.rad2deg(psi)

phi_e, theta_e, psi_e = quat_to_euler312(Q_euler)
phi_r, theta_r, psi_r = quat_to_euler312(Q_rk4)

# 6. 绘图对比
t = np.arange(N) * dt

plt.figure(figsize=(12, 8))
labels = ['Roll φ', 'Pitch θ', 'Yaw Ψ']
for i, lab in enumerate(labels):
    plt.subplot(3, 1, i+1)
    plt.plot(t, [phi_e, theta_e, psi_e][i], label='Euler 1st')
    plt.plot(t, [phi_r, theta_r, psi_r][i], label='RK4', alpha=0.8)
    plt.ylabel(f'{lab} (deg)')
    plt.legend()
plt.xlabel('Time (s)')
plt.tight_layout()
plt.show()