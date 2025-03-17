import numpy as np
import matplotlib.pyplot as plt
import control

# 1. 定义传递函数 G(s)
#    G(s) = 1 / [ s*(s+1)*(0.25s+1) ]
#    先把分母展开： (s+1)*(0.25s+1) = 0.25s^2 + 1.25s + 1
#                   再乘以 s => 0.25s^3 + 1.25s^2 + s
num = [5]
den = [0.05, 0.6, 1, 0]   # 对应 0.25*s^3 + 1.25*s^2 + 1*s + 0

G = control.TransferFunction(num, den)

# 2. 计算增益裕度、相位裕度等
gm, pm, w_gm, w_pm = control.margin(G)

print("============== 计算结果 ==============")
print(f"增益裕度 GM     = {gm:.4f}   (绝对值)")
print(f"相位裕度 PM     = {pm:.2f}   (单位：度)")
print(f"增益交叉频率 wg = {w_gm:.4f} (rad/s)")
print(f"相位交叉频率 wp = {w_pm:.4f} (rad/s)")
