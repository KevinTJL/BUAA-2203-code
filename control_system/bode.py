from cv2 import exp
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 定义传递函数 H(s) = 10 / (s^2 + 2s + 10)
numerator = [5]   # 分子系数
denominator = [0.05,0.6,1,0]  # 分母系数
system = signal.TransferFunction(numerator, denominator)

# 定义更多的频率点
frequencies = np.logspace(-1, 10, num=100000)  # 从 0.1 到 10^6 取 10000 个点

# 计算 Bode 图数据
frequencies, magnitude, phase = signal.bode(system,frequencies)

# 计算幅值裕度和相位裕度
# 幅值裕度：找到相位为 -180° 的频率，计算对应的幅值
phase_margin_index = np.argmin(np.abs(phase + 180))  # 找到相位最接近 -180° 的点
phase_margin_freq = frequencies[phase_margin_index]
gain_margin = magnitude[phase_margin_index]  # 幅值裕度
gain_margin_freq = phase_margin_freq  # 幅值裕度对应的频率

# 相位裕度：找到增益为 0 dB 的频率，计算对应的相位
gain_margin_index = np.argmin(np.abs(magnitude))  # 找到幅值最接近 0 dB 的点
gain_margin_phase = phase[gain_margin_index]  # 相位裕度
gain_margin_freq_n = frequencies[gain_margin_index]  # 相位裕度对应的频率

# 输出幅值裕度和相位裕度
print(f"Kg: {1/(10**(gain_margin / 20))} 绝对值， {1/gain_margin}db at {gain_margin_freq} rad/s")
print(f"Mr: {180 + gain_margin_phase} degrees at {gain_margin_freq_n} rad/s")

# 查找增益为 -3dB 时的频率（开环带宽 WB）
bandwidth_freq = frequencies[np.argmin(np.abs(magnitude + 3))]  # -3dB 对应的频率
print(f"Open-loop Bandwidth (WB): {bandwidth_freq} Hz")

# 绘制幅频特性图
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.semilogx(frequencies, magnitude)  # 对数刻度
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("Bode Plot")
plt.grid(which="both", linestyle="--", linewidth=0.5)

# 手动设置更多的刻度
plt.xticks(np.logspace(-1, 1, num=10))  

# 绘制相频特性图
plt.subplot(2, 1, 2)
plt.semilogx(frequencies, phase)  # 对数刻度
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (degrees)")
plt.grid(which="both", linestyle="--", linewidth=0.5)

# 手动设置更多的刻度
plt.xticks(np.logspace(-1, 1, num=10))  

plt.tight_layout()
plt.show()
