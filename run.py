import cv2
import os
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QPlainTextEdit, QPushButton, QFileDialog, QLabel, QLineEdit
from PyQt5.QtGui import QMovie, QPixmap, QFont
from chaos_encrypt import logistic_encrypt, logistic_decrypt
from evaluation import is_same_img, get_img_entropy, cmp_img_histogram, get_img_corrlation


class AppWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(500, 500)
        self.setWindowTitle("混沌加密-2022-06")

        # 布局
        self.filename = ""
        self.g_layout = QGridLayout(self)
        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        
        # 字体设置
        font_1 = QFont("Microsoft YaHei", 10, 75)
        font_2 = QFont("Microsoft YaHei", 10, 75)
        font_3 = QFont("Microsoft YaHei", 15, 50)

        # 布局内部设置
        self.v1_layout.setContentsMargins(20, 20, 20, 20)
        self.v1_layout.setSpacing(10)
        self.v2_layout.setContentsMargins(20, 20, 20, 20)
        self.v2_layout.setSpacing(10)

        # v1_layout
        btn_encrypt = QPushButton('加密', self)
        btn_encrypt.setObjectName('EncryptBtn')
        btn_encrypt.setFont(font_2)
        btn_encrypt.clicked.connect(self.on_encrypt_click)
        self.v1_layout.addWidget(btn_encrypt)

        btn_decrypt = QPushButton('解密', self)
        btn_decrypt.setObjectName('DecryptBtn')
        btn_decrypt.setFont(font_2)
        btn_decrypt.clicked.connect(self.on_decrypt_click)
        self.v1_layout.addWidget(btn_decrypt)

        self.img_area_1 = QLabel(self)
        self.img_area_1.setFixedSize(200, 200)
        self.img_area_1.setStyleSheet("border:1px solid gray;")
        self.v1_layout.addWidget(self.img_area_1)

        # v2_layout
        btn_select_file = QPushButton('选择文件', self)
        btn_select_file.setObjectName('SelectFileBtn')
        btn_select_file.setFont(font_2)
        btn_select_file.clicked.connect(self.on_select_file_click)
        self.v2_layout.addWidget(btn_select_file)

        # self.filename_area = QLineEdit(self)
        # self.filename_area.setEnabled(False)
        # self.v2_layout.addWidget(self.filename_area)

        # input_hint = QLineEdit(self)
        # input_hint.setText("请在下方输入密钥")
        # input_hint.setFont(font_1)
        # input_hint.setEnabled(False)
        # self.v2_layout.addWidget(input_hint)

        self.input_area = QLineEdit(self)
        self.input_area.setPlaceholderText("请在下方输入密钥")
        self.input_area.setFont(font_1)
        self.v2_layout.addWidget(self.input_area)

        self.img_area_2 = QLabel(self)
        self.img_area_2.setFixedSize(200, 200)
        self.img_area_2.setStyleSheet("border:1px solid gray;")
        self.v2_layout.addWidget(self.img_area_2)

        # 整体是网格布局，网格布局中包含垂直布局
        self.g_layout.addLayout(self.v1_layout, 0, 0, 1, 1)
        self.g_layout.addLayout(self.v2_layout, 0, 1, 1, 2)
        
        self.resultView = QPlainTextEdit(self)
        self.resultView.setFont(font_3)
        self.resultView.setReadOnly(True)
        self.g_layout.addWidget(self.resultView, 1, 0, -1, -1)
        

    # 选择加解密文件
    def on_select_file_click(self):
        f = QFileDialog.getOpenFileName(self, "选择图像", os.getcwd(), "*.jpg;*.png;*.jpeg;*.gif")
        self.filename = f[0]
        if self.filename != "":
            # 展示图片
            # if re.findall(".gif", file_name[0]) != []:
            #     self.add_gif(self.img_area_1, file_name[0])
            #     self.add_gif(self.img_area_2, file_name[0])
            # else:
            self.add_img(self.img_area_1, self.filename)
            self.resultView.appendPlainText(self.get_time() + '选择文件{}'.format(self.filename))


    def on_encrypt_click(self):
        key_str = self.input_area.text()
        if key_str != "":
            self.resultView.appendPlainText(self.get_time() + '加密文件中...')
            self.encrypt_img(key_str)
        else:
            self.resultView.appendPlainText(self.get_time() + '未输入加密密钥！')
        self.input_area.setText("")


    def on_decrypt_click(self):
        key_str = self.input_area.text()
        if key_str != "":
            self.resultView.appendPlainText(self.get_time() + '解密文件中...')
            self.decrypt_img(key_str)
        else:
            self.resultView.appendPlainText(self.get_time() + '未输入解密密钥！')
        self.input_area.setText("")

    def add_gif(self, label, file_name):
        movie = QMovie(file_name)
        label.setMovie(movie)
        movie.start()

    def add_img(self, label, file_name):
        pixmap = QPixmap(file_name).scaled(label.width(), label.height())
        label.setPixmap(pixmap)

    def encrypt_img(self, key_str):
        pos = self.filename.rfind(".")
        encrypted_path = self.filename[ : pos] + "-enc.png"
        # 调用WorkThread线程
        self.work_thread = WorkThread()
        self.work_thread.update_signal.connect(self.work_callback)
        self.work_thread.encrypted = True
        self.work_thread.key_str = key_str
        self.work_thread.path_1 = self.filename
        self.work_thread.path_2 = encrypted_path
        self.work_thread.start()

    def decrypt_img(self, key_str):
        pos = self.filename.rfind(".")
        decrypted_path = self.filename[ : pos] + "-dec.png"
        # 调用WorkThread线程
        self.work_thread = WorkThread()
        self.work_thread.update_signal.connect(self.work_callback)
        self.work_thread.encrypted = False
        self.work_thread.key_str = key_str
        self.work_thread.path_1 = self.filename
        self.work_thread.path_2 = decrypted_path
        self.work_thread.start()
    
    def get_time(self):
        now = int(time.time())
        #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        timeArray = time.localtime(now)
        otherStyleTime = "[" + time.strftime("%Y-%m-%d %H:%M:%S", timeArray) + "]  "
        return otherStyleTime

    # WorkThread结束后的回调函数
    def work_callback(self, path, encrypted):
        self.add_img(self.img_area_2, path)
        if encrypted:
            self.resultView.appendPlainText(self.get_time() + '加密文件完毕！')
        else:
            self.resultView.appendPlainText(self.get_time() + '解密文件完毕！')


# 加解密图片线程
class WorkThread(QThread):
    # 回调函数接受的信号
    update_signal = pyqtSignal(str, bool)
    # 接收UI线程的参数
    encrypted = None
    key_str = None
    path_1 = None
    path_2 = None
    def __int__(self):
        super(WorkThread, self).__init__()
    def run(self):
        if self.encrypted == True:
            logistic_encrypt(self.key_str, self.path_1, self.path_2)
        else:      
            logistic_decrypt(self.key_str, self.path_1, self.path_2)
        self.update_signal.emit(self.path_2, self.encrypted)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

    # 是否为rgb图片
    # print(os.getcwd()) #获取当前工作目录路
    # key_str = "abc123"
    # file_path = "./img/lena.jpg"
    # img = cv2.imread(file_path)
    # rgb = True if len(img.shape) == 3 else False
    # print(rgb, img.shape)
    # encrypted_path = "./img/enc.png"
    # decrypted_path = "./img/dec.png"
    # # logistic_encrypt(key_str, file_path, encrypted_path)
    # # logistic_decrypt(key_str, encrypted_path, decrypted_path)

    # # 检验图片解密是否正确
    # # print("是否原样恢复?", is_same_img(file_path, decrypted_path))
    
    # # 评估加密性能——直方图，像素相关性，图像熵
    # # cmp_img_histogram(file_path, encrypted_path, rgb)
    # # cmp_img_histogram(file_path, encrypted_path, rgb=False)
    # print("原始图片的熵",get_img_entropy(file_path, rgb))
    # print("加密图片的熵",get_img_entropy(encrypted_path, rgb))
    # # print(get_img_corrlation(file_path, rgb))
    # # print(get_img_corrlation(encrypted_path, rgb))