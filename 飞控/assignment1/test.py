from scipy.io import loadmat

# 加上 struct_as_record=False, squeeze_me=True
mat = loadmat('WNBB.mat', struct_as_record=False, squeeze_me=True)
print("顶层键：", mat.keys())

# 直接取出 struct 对象
ms = mat['WNBBSHOW']
print("WNBBSHOW 类型：", type(ms))

# 如果是一个对象，就查看它的属性字典
if hasattr(ms, '__dict__'):
    print("字段列表：", ms.__dict__.keys())
else:
    # 如果是 ndarray，取出元素再看
    ms0 = ms[0] if isinstance(ms, (list, tuple)) else ms
    print("查看 ms0 类型：", type(ms0))
    print("属性列表：", dir(ms0))

# 假设字段名字是 'p','q','r'，那就直接：
p = ms.p.flatten()
q = ms.q.flatten()
r = ms.r.flatten()

print("样本数：", len(p), len(q), len(r))
