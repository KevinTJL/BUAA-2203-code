import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 1. 定义连续系统：D(s)=1/(s+1)
num_c = [1.0]
den_c = [1.0, 1.0]

# 2. 参数
Ts_list = [0.1, 0.4]
w      = np.linspace(0, 20, 41)  # rad/s

for Ts in Ts_list:
    # 3. 离散化
    methods = {
        'ZOH'     : signal.cont2discrete((num_c, den_c), Ts, method='zoh'),
        'Forward' : signal.cont2discrete((num_c, den_c), Ts, method='forward'),
        'Backward': signal.cont2discrete((num_c, den_c), Ts, method='backward'),
        'Matched' : signal.cont2discrete((num_c, den_c), Ts, method='matched'),
        'Tustin'  : signal.cont2discrete((num_c, den_c), Ts, method='bilinear'),
        'Tustin_PW': signal.cont2discrete((num_c, den_c), Ts,
                                           method='bilinear',
                                           prewarp_frequency=1.0)
    }

    # 4. 计算连续频率响应
    Hc = 1 / (1 + 1j*w)

    # 5. 计算各离散系统的频率响应
    Hd = {}
    for name, (num_d, den_d, dt) in methods.items():
        # freqz 中 worN 接收数字角频率(rad/sample)=ω*Ts
        _, h = signal.freqz(num_d.flatten(), den_d.flatten(), worN=w*Ts)
        Hd[name] = h

    # 6. 绘图：连续 + 6 离散
    plt.figure(figsize=(8,6))
    for name, h in Hd.items():
        plt.semilogx(w, 20*np.log10(np.abs(h)), label=name)
    plt.semilogx(w, 20*np.log10(np.abs(Hc)), 'k-', lw=1.5, label='Continuous')
    plt.title(f'T = {Ts:.1f}s: Continuous vs. All Discrete')
    plt.xlabel('ω (rad/s)'); plt.ylabel('Magnitude (dB)')
    plt.grid(True); plt.legend(loc='best')

    # 7. 绘图：仅 6 离散
    plt.figure(figsize=(8,6))
    for name, h in Hd.items():
        plt.semilogx(w, 20*np.log10(np.abs(h)), label=name)
    plt.title(f'T = {Ts:.1f}s: Only Discrete Methods')
    plt.xlabel('ω (rad/s)'); plt.ylabel('Magnitude (dB)')
    plt.grid(True); plt.legend(loc='best')

plt.show()
