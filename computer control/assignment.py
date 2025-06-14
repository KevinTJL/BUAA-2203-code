import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import cont2discrete, freqs, freqz, impulse, dimpulse

# ─── 1. 定义连续系统 D(s) ────────────────────────────────
# TODO: 将下面 num 和 den 替换为题目中 D(s) 的分子、分母多项式系数
num = [ 1 ]  
den = [ 1, 1 ]

# 连续频率范围：0 ~ 20 rad/s 共 41 点
w_cont = np.linspace(0, 20, 41)

# ─── 2. 离散化方法列表（去掉 matched） ────────────────────
methods = {
    'zoh'           : {'method': 'zoh'},
    'backward_diff' : {'method': 'backward_diff'},
    'forward_diff'  : {'method': 'euler'},
    'tustin'        : {'method': 'bilinear'},
    'prewarp'       : {'method': 'bilinear', 'alpha': 1.0},
}

Ts_list = [0.1, 0.4]

for Ts in Ts_list:
    systems = {}

    # 先用 cont2discrete 生成五种方法
    for name, opts in methods.items():
        num_d, den_d, dt = cont2discrete((num, den), Ts, **opts)
        systems[name] = {
            'num': num_d.flatten(),
            'den': den_d.flatten(),
            'dt' : dt
        }

    # 手动实现零极点匹配（matched）
    # 连续系统的零、极点
    zc = np.roots(num)
    pc = np.roots(den)
    # 映射到 z 平面
    zd = np.exp(zc * Ts)
    pd = np.exp(pc * Ts)
    # 求多项式系数
    den_d = np.poly(pd)
    num_d = np.poly(zd)
    num_d = np.atleast_1d(num_d)
    den_d = np.atleast_1d(den_d)
    # 调整增益，使 H_d(1) = H_c(0)
    k_c  = np.polyval(num, 0) / np.polyval(den, 0)
    k_d0 = np.polyval(num_d, 1) / np.polyval(den_d, 1)
    num_d = num_d * (k_c / k_d0)
    systems['matched'] = {'num': num_d, 'den': den_d, 'dt': Ts}

    # ─── 3. 绘图（与原脚本相同） ─────────────────────────────
    # 3.1 零极点
    plt.figure(figsize=(6,6))
    for name, sys in systems.items():
        z = np.roots(sys['num'])
        p = np.roots(sys['den'])
        plt.plot(np.real(z), np.imag(z), 'o', label=f'{name} zeros')
        plt.plot(np.real(p), np.imag(p), 'x', label=f'{name} poles')
    plt.title(f'Zeros & Poles (T={Ts}s)')
    plt.xlabel('Real'); plt.ylabel('Imag'); plt.grid(True)
    plt.axis('equal'); plt.legend(); plt.show()

    # 3.2 幅相特性对比
    # 连续
    _, Hc = freqs(num, den, w_cont)

    fig, (axm, axp) = plt.subplots(2,1,sharex=True,figsize=(8,6))
    axm.plot(w_cont, 20*np.log10(np.abs(Hc)), 'k-', label='Continuous')
    axp.plot(w_cont, np.angle(Hc, deg=True), 'k-')
    for name, sys in systems.items():
        w_dig = w_cont * Ts
        _, Hd = freqz(sys['num'], sys['den'], worN=w_dig)
        axm.plot(w_cont, 20*np.log10(np.abs(Hd)), label=name)
        axp.plot(w_cont, np.angle(Hd, deg=True), label=name)
    axm.set_ylabel('Mag (dB)'); axp.set_ylabel('Phase (°)'); axp.set_xlabel('ω (rad/s)')
    axm.set_title(f'Bode (T={Ts}s)'); axm.grid(True); axp.grid(True); axm.legend(fontsize='small')
    plt.tight_layout(); plt.show()

    # 3.3 单位脉冲响应
    # 连续
    t_c, y_c = impulse((num, den), T=np.linspace(0, 4, 1000))
    plt.figure()
    plt.plot(t_c, y_c, 'k-'); plt.title('Continuous Impulse'); plt.xlabel('s'); plt.grid(True); plt.show()

    # 离散
    n_pts = int(4 / Ts) + 1
    for name, sys in systems.items():
        t_d, y_d = dimpulse((sys['num'], sys['den'], sys['dt']), n=n_pts)
        t_d = np.squeeze(t_d); y_d = np.squeeze(y_d)
        plt.figure()
        plt.stem(t_d, y_d, basefmt=" "); plt.title(f'Impulse ({name}, T={Ts}s)')
        plt.xlabel('s'); plt.grid(True); plt.show()