import sympy as sp

def steady_state_error(G, input_type):
    """
    计算任意开环传递函数在单位负反馈下的稳态误差

    参数：
    G: sympy.Expr
        开环传递函数 (G(s))，形式为符号表达式
    input_type: str
        输入信号类型，可选值为 '1/s', '1/s^2', '1/s^3'

    返回：
    float
        稳态误差
    """
    # 定义复数变量 s
    s = sp.symbols('s')

    # 闭环传递函数 T(s) = G(s) / (1 + G(s))
    T = G / (1 + G)

    # 确定输入信号的形式
    if input_type == '1/s':
        R = 1 / s
    elif input_type == '1/s^2':
        R = 1 / s**2
    elif input_type == '1/s^3':
        R = 1 / s**3
    else:
        raise ValueError("Invalid input_type. Must be '1/s', '1/s^2', or '1/s^3'.")

    # 稳态误差 e_ss = lim(s -> 0, s * (1 - T(s)) * R(s))
    E_s = s * (1 - T) * R
    e_ss = sp.limit(E_s, s, 0)

    return e_ss

# 示例使用
if __name__ == "__main__":
    # 定义开环传递函数 G(s)
    s = sp.symbols('s')
    G = 3 * (2-s) / ((s - 1) * (s + 4))

    # 计算稳态误差
    for input_type in ['1/s', '1/s^2', '1/s^3']:
        e_ss = steady_state_error(G, input_type)
        print(f"输入信号为 {input_type} 时的稳态误差: {e_ss}")