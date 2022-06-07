import numpy as np
import time
import cv2
# 导入本项目的包
from mapping_generate import logistic_map
from key_generate import get_key
from pix_replace import pix_seq_permutation, pix_seq_inv_permutation
from arnold_permutate import arnold_bit_permutation, arnold_bit_inv_permutation


# 加密
def logistic_encrypt(key_str, file_path, encrypted_path):
    x0, seed, start_pos = get_key(key_str)
    start = time.time()

    # 图片转为序列处理
    img = np.array(cv2.imread(file_path))
    raw_shape = img.shape
    encrypted_img = img.flatten()
    # 像素值替代
    encrypted_img = pix_seq_permutation(encrypted_img, seed)
    # 混沌加密
    length = encrypted_img.shape[0]
    mapping = logistic_map(x0, length, start_pos)
    print(mapping.dtype, encrypted_img.dtype)
    encrypted_img = mapping[ :  length] ^ encrypted_img
    # Arnold 8*8比特置乱 
    encrypted_img = arnold_bit_permutation(encrypted_img)
    # 加密并记录密钥信息
    encrypted_img = encrypted_img.reshape(raw_shape)
    cv2.imwrite(encrypted_path, encrypted_img)

    end = time.time()
    print("加密成功，耗时{:.2f}s\n".format(end - start))


# 解密
def logistic_decrypt(key_str, encrypted_path, decrypted_path):
    x0, seed, start_pos = get_key(key_str)
    start = time.time()
 
    # 图片转为序列处理
    img = np.array(cv2.imread(encrypted_path))
    raw_shape = img.shape
    decrypted_img = img.flatten()
    # Arnold 8*8比特逆置乱 
    decrypted_img = arnold_bit_inv_permutation(decrypted_img)
    # 混沌解密
    length = decrypted_img.shape[0]
    mapping = logistic_map(x0, length, start_pos)
    decrypted_img = mapping[ : length] ^ decrypted_img
    # 像素值替代
    decrypted_img = decrypted_img.flatten()
    decrypted_img = pix_seq_inv_permutation(decrypted_img, seed)
    # 保存解密图片
    decrypted_img = decrypted_img.reshape(raw_shape)
    cv2.imwrite(decrypted_path, decrypted_img)
    
    end = time.time()
    print("解密成功，耗时{:.2f}s\n".format(end - start))