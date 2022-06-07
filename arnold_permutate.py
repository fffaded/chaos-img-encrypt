import numpy as np

# 比特序列置乱：将输入像素每8个像素进行比特置乱，8个像素按比特进行arnold置乱（8*8方阵）
def arnold_bit_permutation(ori_seq, block_size=8):
    ori_seq = np.array(ori_seq)
    new_seq = np.array([], dtype=np.uint8)
    temp = np.array([], dtype=np.uint8)
    block_count, remainder = divmod(len(ori_seq), 8)[0], divmod(len(ori_seq), 8)[1]
    if remainder != 0:
        temp = ori_seq[- remainder : ]
    for i in range(block_count):
        block = pix_to_bits(ori_seq[i * block_size : (i + 1) * block_size], block_size).reshape((block_size, block_size))
        block = arnold_permutation(block).flatten()
        block = bits_to_pix(block, block_size * block_size)
        new_seq = np.append(new_seq, block)
    new_seq = np.append(new_seq, temp)
    return np.array(new_seq, dtype=np.uint8)


# 比特序列逆置乱：每8个像素按比特进行arnold逆置乱（8*8方阵）
def arnold_bit_inv_permutation(ori_seq, block_size=8):
    ori_seq = np.array(ori_seq)
    new_seq = np.array([], dtype=np.uint8)
    temp = np.array([], dtype=np.uint8)
    block_count, remainder = divmod(len(ori_seq), 8)[0], divmod(len(ori_seq), 8)[1]
    if remainder != 0:
        temp = ori_seq[- remainder : ]
    for i in range(block_count):
        block = pix_to_bits(ori_seq[i * block_size : (i + 1) * block_size], block_size).reshape((block_size, block_size))
        block = arnold_inv_permutation(block).flatten()
        block = bits_to_pix(block, block_size * block_size)
        new_seq = np.append(new_seq, block)
    new_seq = np.append(new_seq, temp)
    return np.array(new_seq, dtype=np.uint8)


# Arnold方阵置乱
def arnold_permutation(img, times=10):
    # if img.shape[0] != img.shape[1]:
    #     img = array_padding(img, rgb)
    new_img = np.array(img)
    for _ in range(times):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                new_i = (i + j) % img.shape[0]
                new_j = (i + 2 * j) % img.shape[0]
                new_img[new_i][new_j] = img[i][j]
    return new_img 


# Arnold逆置换
def arnold_inv_permutation(img, times=10):
    raw_img = np.array(img)
    for _ in range(times):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                raw_i = (2 * i - j) % img.shape[0]
                raw_j = (- i + j) % img.shape[0]
                raw_img[raw_i][raw_j] = img[i][j]
    return raw_img


# 每8个随机bit转为一个0-255像素值
def bits_to_pix(bits, bits_len):
    pixels = np.array([], dtype=np.uint8)
    for i in range(int(bits_len / 8)):
        pixel = 0
        for j in range(8):
            pixel += bits[i * 8 + j] * ( 2 ** (7 - j)) 
        pixels = np.append(pixels, pixel)
    return pixels


# 一个0-255像素值转为8个比特
def pix_to_bits(pixels, pixels_len):
    bits = np.array([], dtype=np.uint8)
    for i in range(pixels_len):
        pixel = pixels[i]
        for j in range(8):
            bit, pixel = divmod(pixel, 2 ** (7 - j))
            bits = np.append(bits, bit)
    return bits