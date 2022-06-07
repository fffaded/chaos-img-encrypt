import numpy as np
import math

# 获得指定长度的Logistic混沌映射序列（改进的Logistic映射，分布均匀）
def logistic_map(x0, length=10, start=10000):
    logistic_map_sequence = []
    logistic_map_sequence.append(x0)
    for _ in range(length + start - 1):
        x0 = 4.0 * x0 * (1 - x0)
        logistic_map_sequence.append(x0)

    # 如果要完成二值映射，需要将序列中的转换为[0,255]，对应与一个字节进行异或加密
    logistic_map_sequence = (2.0 / math.pi) * np.arcsin(np.sqrt(logistic_map_sequence))
    logistic_map_sequence = np.array((np.array(logistic_map_sequence) * 255))
    # logistic_map_sequence[logistic_map_sequence < 0.5] = 0
    # logistic_map_sequence[logistic_map_sequence >= 0.5] = 1
    # mapping = np.zeros(length, np.uint8)
    # for i in range(length):
    #     mapping[i] = bits_to_pix(logistic_map_sequence[start + i * 8 : start + i * 8 + 8])
    # 查看生成序列的概率分布
    # plt.hist(logistic_map_sequence, 256, [0,256])
    # print(np.array(list(range(length))).shape, logistic_map_sequence[start:].shape)
    # plt.scatter(np.array(list(range(length))), logistic_map_sequence[start:], s=0.5, c='black')
    # plt.show()
    return np.array(logistic_map_sequence[start : ], dtype=np.uint8)