import numpy as np
import hashlib

# 获取加密所需要的的参数（混沌序列起始值，随机种子值，混沌序列起始位置）
def get_key(key_str, x0_digits=16, round_digits=6):
    key_hash = hashlib.sha256(str(key_str).encode(encoding='UTF-8')).hexdigest()
    np.random.seed(int(key_hash[: 4], 16))
    x0 = round(np.random.rand(), x0_digits)
    np.random.seed(int(key_hash[4 : 8], 16))
    seed = int(round(np.random.rand(), round_digits) * 1000000)
    start_pos = int(key_hash[8 : 12], 16)
    # return 0.408417, 772357, 51824
    # return 0.408416, 772357, 51824
    # return 0.408417, 772355, 51824
    return 0.408417, 772357, 51825
    # return x0, seed, start_pos


# 测试用
if __name__ == "__main__":
    print(get_key("abc123"))

