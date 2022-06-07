import numpy as np

# 像素值替换
def pix_seq_permutation(ori_seq, seed):
    p_key = np.array([i for i in range(256)])
    p_value = np.array(p_key)
    np.random.seed(seed)
    np.random.shuffle(p_key)
    p = dict(zip(p_key, p_value))
    new_seq = np.array([])
    for pix in ori_seq:
        new_seq = np.append(new_seq, p[pix])
    return np.array(new_seq, dtype=np.uint8)


# 像素值逆替换
def pix_seq_inv_permutation(new_seq, seed):
    p_key = np.array([i for i in range(256)])
    p_value = np.array(p_key)
    np.random.seed(seed)
    np.random.shuffle(p_key)
    inv_p = dict(zip(p_value, p_key))
    ori_seq = np.array([])
    for pix in new_seq:
        ori_seq = np.append(ori_seq, inv_p[pix])
    return np.array(ori_seq, dtype=np.uint8)