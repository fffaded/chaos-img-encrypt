import cv2
from matplotlib import pyplot as plt
import numpy as np

# 允许中文
plt.rcParams['font.sans-serif'] = ['SimHei']

# 不同通道直方图比较
def cmp_img_histogram(file_1, file_2, rgb):
    # RGB读取
    if rgb:
        img_1 = cv2.imread(file_1)
        img_2 = cv2.imread(file_2)
        # 绘制不同通道的直方图,opencv默认读取顺序是BGR
        plt.subplot(2,3,1)
        plt.hist(img_1[:,:,0].ravel(), 256, [0,256])
        plt.title("B")
        plt.subplot(2,3,2)
        plt.hist(img_1[:,:,1].ravel(), 256, [0,256])
        plt.title("G")
        plt.subplot(2,3,3)
        plt.hist(img_1[:,:,2].ravel(), 256, [0,256])
        plt.title("R")
        plt.subplot(2,3,4)
        plt.hist(img_2[:,:,0].ravel(), 256, [0,256])
        plt.title("B")
        plt.subplot(2,3,5)
        plt.hist(img_2[:,:,1].ravel(), 256, [0,256])
        plt.title("G")
        plt.subplot(2,3,6)
        plt.hist(img_2[:,:,2].ravel(), 256, [0,256])
        plt.title("R")
        plt.suptitle("RGB histogram")
        plt.show()
    # 灰度读取
    else:
        img_1 = cv2.imread(file_1, 0)
        img_2 = cv2.imread(file_2, 0)
        # 绘制不同通道的直方图
        plt.subplot(1,2,1)
        plt.hist(img_1.ravel(), 256, [0,256])
        plt.subplot(1,2,2)
        plt.hist(img_2.ravel(), 256, [0,256])
        plt.suptitle("Gray histogram")
        plt.show()


# 得到图像熵(灰度读取)
def get_img_entropy(file_path, rgb):
    img_entropy = []
    # RGB图像分别计算三个通道的图像熵
    if rgb:
        img = cv2.imread(file_path)
        for channel in range(3):
            hist = cv2.calcHist(img[:, :, channel], [0], None, [255], [0,255])
            hist = hist / hist.sum()
            hist = np.array([i for i in hist if i[0]!=0])
            img_entropy.append((-hist * np.log2(hist)).sum())
    else:
        img = cv2.imread(file_path)
        hist = cv2.calcHist([img], [0], None, [255], [0,255])
        hist = hist / hist.sum()
        hist = np.array([i for i in hist if i[0]!=0])
        img_entropy.append((-hist * np.log2(hist)).sum())
    return img_entropy


# 对比图片每个像素值是否相同
def is_same_img(file_1, file_2):
    img_1 = cv2.imread(file_1)
    img_2 = cv2.imread(file_2)
    is_same = (img_1 == img_2).all()
    return is_same

# 获取两个不同序列的想关
def get_seq_corrlation(seq_1, seq_2):
    return np.corrcoef(seq_1, seq_2)[1][0],

# 相邻像素相关性衡量：在水平,垂直,对角线方向分别选取1000个相邻像素对(假设图像至少是1000个像素)
def get_img_corrlation(file_path, rgb, N=1000):
    if rgb:
        img = cv2.imread(file_path, 1)
        h, w, _ = img.shape
        x = np.random.randint(0, h-1, N)
        y = np.random.randint(0, w-1, N)
        # print(img.shape, x.shape, y.shape)
        # 得到水平、垂直和对角线方向相邻像素，shape为(N，3)
        pix, pix_h, pix_v, pix_d = np.array([img[x[0], y[0]]]), np.array([img[x[0], y[0]+1]]), np.array([img[x[0]+1, y[0]]]), np.array([img[x[0]+1, y[0]+1]])
        for i in range(1, N):
            pix = np.vstack((pix, img[x[i], y[i]]))
            pix_h = np.vstack((pix_h, img[x[i], y[i]+1]))
            pix_v = np.vstack((pix_v, img[x[i]+1, y[i]]))
            pix_d = np.vstack((pix_d, img[x[i]+1, y[i]+1]))
        # 做像素相关性图
        plt.suptitle("像素相关性图")
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 2, 1)
        plt.title("图像")
        plt.imshow(img[:,:,(2,1,0)])
        plt.subplot(2, 2, 2)
        plt.title("B Channel")
        plt.scatter(pix[:,0], pix_h[:,0], s=1, c='blue')
        plt.subplot(2, 2, 3)
        plt.title("G Channel")
        plt.scatter(pix[:,1], pix_h[:,1], s=1, c='green')
        plt.subplot(2, 2, 4)
        plt.title("R Channel")
        plt.scatter(pix[:,2], pix_h[:,2], s=1, c='red')
        plt.show()
        # 计算与三个相邻像素的相关系数
        corr_h = np.array([
            np.corrcoef(pix[:, 0], pix_h[:, 0])[1][0],
            np.corrcoef(pix[:, 1], pix_h[:, 1])[1][0],
            np.corrcoef(pix[:, 2], pix_h[:, 2])[1][0],
        ])
        corr_v = np.array([
            np.corrcoef(pix[:, 0], pix_v[:, 0])[1][0],
            np.corrcoef(pix[:, 1], pix_v[:, 1])[1][0],
            np.corrcoef(pix[:, 2], pix_v[:, 2])[1][0],
        ])
        corr_d = np.array([
            np.corrcoef(pix[:, 0], pix_d[:, 0])[1][0],
            np.corrcoef(pix[:, 1], pix_d[:, 1])[1][0],
            np.corrcoef(pix[:, 2], pix_d[:, 2])[1][0],
        ])

    else:
        img = cv2.imread(file_path, 0)
        h, w = img.shape
        x = np.random.randint(0, h-1, N)
        y = np.random.randint(0, w-1, N)
        # print(img.shape, x.shape, y.shape)
        # 得到水平、垂直和对角线方向相邻像素，shape为(N，3)
        pix, pix_h, pix_v, pix_d = np.array([img[x[0], y[0]]]), np.array([img[x[0], y[0]+1]]), np.array([img[x[0]+1, y[0]]]), np.array([img[x[0]+1, y[0]+1]])
        print(pix, pix_h)
        for i in range(1, N):
            pix = np.vstack((pix, img[x[i], y[i]]))
            pix_h = np.vstack((pix_h, img[x[i], y[i]+1]))
            pix_v = np.vstack((pix_v, img[x[i]+1, y[i]]))
            pix_d = np.vstack((pix_d, img[x[i]+1, y[i]+1]))
        # 做像素相关性图    
        plt.suptitle("像素相关性图")
        plt.subplot(1, 2, 1)
        plt.title("图像")
        plt.imshow(img, cmap="gray")
        plt.subplot(1, 2, 2)
        plt.title("Gray Channel")
        plt.scatter(pix, pix_h, s=1, c='gray')
        plt.show()
        # 计算与三个相邻像素的相关系数
        corr_h = np.array([
            np.corrcoef(pix[:, 0], pix_h[:, 0])[1][0],
        ])
        corr_v = np.array([
            np.corrcoef(pix[:, 0], pix_v[:, 0])[1][0],
        ])
        corr_d = np.array([
            np.corrcoef(pix[:, 0], pix_d[:, 0])[1][0],
        ])
    
    return corr_h, corr_v, corr_d    