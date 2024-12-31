import numpy as np
from PIL.ImageFont import ImageFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QAbstractItemView, QApplication
from matplotlib.pyplot import connect
from ultralytics import YOLO
import sys
import time
import cv2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#数据集的自增：
#这里一开始是想找一个关于猕猴桃的病害图片集，但是相关图片集几乎没有，于是采用在互联网种找图片下载后进行打标签的工作，打标签工具使用labelimg



plant_list = ["苹果黑星病","苹果黑腐病","苹果桧胶锈病","苹果健康叶","蓝莓健康叶","樱桃白粉病","樱桃健康叶","玉米灰斑病","玉米普通锈病","玉米叶枯病","玉米健康叶","葡萄黑腐病","葡萄黑痘病","葡萄叶枯病","葡萄健康叶","柑橘黄龙病","桃细菌性穿孔病","桃树健康叶","甜椒细菌性叶斑病","甜椒健康叶","土豆早疫病","土豆晚疫病","土豆健康叶","树莓健康叶","大豆健康叶","南瓜白粉病","草莓炭疽病","草莓健康叶","番茄细菌性斑疹病","番茄早疫病","番茄晚疫病","番茄叶霉病","番茄灰叶斑病","番茄二斑叶螨",
 "番茄斑点病","番茄叶黄病毒病","番茄花叶病毒病","番茄健康叶"]


class Ui_xinxi(object):
    def setupUi(self, xinxi):
        self.xinxi = xinxi
        xinxi.setObjectName("xinxi")
        xinxi.resize(351, 166)
        self.label = QtWidgets.QLabel(xinxi)
        self.label.setGeometry(QtCore.QRect(40, 50, 271, 31))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(xinxi)
        self.pushButton.setGeometry(QtCore.QRect(240, 130, 88, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(xinxi)
        QtCore.QMetaObject.connectSlotsByName(xinxi)

    def retranslateUi(self, xinxi):
        _translate = QtCore.QCoreApplication.translate
        xinxi.setWindowTitle(_translate("xinxi", "信息"))
        self.label.setText(_translate("xinxi", "这是一个基于yolo11的病虫害识别系统，\n""可识别38种农业病害。"))
        self.pushButton.setText(_translate("xinxi", "确定"))

class XinxiWindow(QDialog, Ui_xinxi):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

class Ui_MainWindow(object):

    def __init__(self):
        # 初始化模型和其它成员变量
        self.model = YOLO("./ultralytics-main/runs/train/yolo11n_train/weights/best.pt")  # 加载YOLO模型
        self.model(np.zeros((48, 48, 3)))  # 预加载模型
        # # self.fontC = ImageFont.truetype("Font/platech.ttf", 25, 0)
        # self.org_path = None
        # self.results = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 724)
        MainWindow.setMinimumSize(QtCore.QSize(1060, 724))
        MainWindow.setMaximumSize(QtCore.QSize(1060, 724))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1060, 724)
            MainWindow.setMinimumSize(QtCore.QSize(1060, 724))
            MainWindow.setMaximumSize(QtCore.QSize(1060, 724))
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(220, 0, 271, 43))
            self.label.setMaximumSize(QtCore.QSize(16777215, 43))
            self.label.setObjectName("label")

            # 检测视图区
            self.img_label = QtWidgets.QLabel(self.centralwidget)
            self.img_label.setGeometry(QtCore.QRect(30, 50, 681, 421))
            self.img_label.setMinimumSize(QtCore.QSize(531, 311))
            self.img_label.setStyleSheet("background-color: rgb(247, 255, 255);")
            self.img_label.setObjectName("img_label")

            # 继续设置其他控件
            ...

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 0, 271, 43))
        self.label.setMaximumSize(QtCore.QSize(16777215, 43))
        self.label.setObjectName("label")

        #检测视图区
        self.img_label = QtWidgets.QLabel(self.centralwidget)
        self.img_label.setGeometry(QtCore.QRect(30, 50, 681, 421))
        self.img_label.setMinimumSize(QtCore.QSize(531, 311))
        self.img_label.setStyleSheet("background-color: rgb(247, 255, 255);")
        self.img_label.setObjectName("img_label")


        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 490, 721, 211))
        self.groupBox.setMinimumSize(QtCore.QSize(631, 171))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 263))

        # 识别结果列表
        self.restults_table = QtWidgets.QTableWidget(self.groupBox)
        self.restults_table.setGeometry(QtCore.QRect(10, 20, 701, 181))
        self.restults_table.setMaximumSize(QtCore.QSize(16777215, 257))
        self.restults_table.setStyleSheet("")
        self.restults_table.setObjectName("restults_table")
        self.restults_table.setColumnCount(5)
        self.restults_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.restults_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.restults_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.restults_table.setColumnWidth(1, 200)
        self.restults_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.restults_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.restults_table.setHorizontalHeaderItem(4, item)
        self.restults_table.horizontalHeader().setCascadingSectionResizes(False)
        self.restults_table.horizontalHeader().setStretchLastSection(True)
        self.restults_table.verticalHeader().setStretchLastSection(False)
        self.restults_table.setAlternatingRowColors(True)  # 表格背景交替


        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(740, 50, 301, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.verticalLayout.setObjectName("verticalLayout")

        self.uploadbutton1 = QtWidgets.QPushButton(self.groupBox_2)                 #图片控件
        self.uploadbutton1.setObjectName("uploadbutton1")
        self.uploadbutton1.clicked.connect(self.open_img)

        self.verticalLayout.addWidget(self.uploadbutton1)

        self.uploadbutton2 = QtWidgets.QPushButton(self.groupBox_2)
        self.uploadbutton2.setObjectName("uploadbutton2")
        self.uploadbutton2.clicked.connect(self.open_video)

        self.verticalLayout.addWidget(self.uploadbutton2)

        self.uploadbutton3 = QtWidgets.QPushButton(self.groupBox_2)
        self.uploadbutton3.setObjectName("uploadbutton3")
        self.uploadbutton3.clicked.connect(self.open_camera)

        self.verticalLayout.addWidget(self.uploadbutton3)

        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(740, 200, 301, 401))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 用时显示区
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)                #用时显示文字
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.time_label = QtWidgets.QLabel(self.groupBox_3)             #显示用时控件
        self.time_label.setText("")
        self.time_label.setObjectName("time_label")
        self.horizontalLayout.addWidget(self.time_label)

        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #目标数目控件
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)                #显示文字
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.num_label = QtWidgets.QLabel(self.groupBox_3)              #显示数目
        self.num_label.setText("")
        self.num_label.setObjectName("num_label")
        self.horizontalLayout_2.addWidget(self.num_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)

        #目标选择控件
        self.comboBox = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox.setObjectName("comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)

        #当前类型显示
        self.name_label = QtWidgets.QLabel(self.groupBox_3)
        self.name_label.setText("")
        self.name_label.setObjectName("name_label")

        self.horizontalLayout_4.addWidget(self.name_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)

        #当前置信度显示
        self.con_label = QtWidgets.QLabel(self.groupBox_3)
        self.con_label.setText("")
        self.con_label.setObjectName("con_label")

        self.horizontalLayout_5.addWidget(self.con_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(830, 620, 111, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.action1_0_0 = QtWidgets.QAction(MainWindow)
        self.action1_0_0.setObjectName("action1_0_0")

        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action.triggered.connect(self.open_new_window)

        self.menu.addAction(self.action1_0_0)
        self.menu_2.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "植物病虫害识别系统"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">植物病虫害识别系统</span></p></body></html>"))

        self.img_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">请选择文件类型</p></body></html>"))

        self.groupBox.setTitle(_translate("MainWindow", "检测结果与位置信息"))
        item = self.restults_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "序号"))
        item = self.restults_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "文件地址"))
        item = self.restults_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "类别"))
        item = self.restults_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "置信度"))
        item = self.restults_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "位置"))

        self.groupBox_2.setTitle(_translate("MainWindow", "文件类型"))
        self.uploadbutton1.setText(_translate("MainWindow", "图片"))
        self.uploadbutton2.setText(_translate("MainWindow", "视频"))
        self.uploadbutton3.setText(_translate("MainWindow", "摄像头"))

        self.groupBox_3.setTitle(_translate("MainWindow", "识别结果"))
        self.label_3.setText(_translate("MainWindow", "用时："))
        self.label_4.setText(_translate("MainWindow", "目标数目："))
        self.label_8.setText(_translate("MainWindow", "目标选择："))
        self.label_6.setText(_translate("MainWindow", "类型："))
        self.label_7.setText(_translate("MainWindow", "置信度："))

        self.pushButton.setText(_translate("MainWindow", "退出"))


        self.menu.setTitle(_translate("MainWindow", "版本"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))

        self.action1_0_0.setText(_translate("MainWindow", "1.0.0"))
        self.action.setText(_translate("MainWindow", "信息"))

    def open_new_window(self):
        self.xinxi_window = XinxiWindow()  # 实例化 XinxiWindow
        self.xinxi_window.show()  # 显示新窗口

    def close_window(self):
        QApplication.quit()  # 完全退出程序

    def upload_image(self):
        try:
            print("upload_image called")
            options = QFileDialog.Options()
            # 这里不能以self做parent的值，因为QFileDialog.getOpenFileName 方法的第一个参数 parent 期望的是一个继承自 QWidget 的实例，
            # 而 Ui_MainWindow 并没有直接继承 QWidget，它只是一个 UI 布局的描述类，具体来说，Ui_MainWindow 类并没有继承 QWidget，它只是一个纯粹的类来帮助设置 UI 的布局。
            # 在 setupUi() 方法中，MainWindow（即 MainWindow 或者其他窗口实例）才是实际的 QWidget 对象。因此，当你传递 self 给 QFileDialog 时，
            # 它实际上是传递了一个 Ui_MainWindow ，而非一个窗口类的实例，这就会导致错误。所以这里应将MainWindow作为self保存，然后再传入getOpenFileName。
            img_path, _ = QFileDialog.getOpenFileName(self.MainWindow, "选择图片", "","所有文件 (*);;图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)",options=options)
            print(f"选择的图片路径: {img_path}")
            if not img_path:
                print("没有选择图片")
                return
        except Exception as e:
            print(f"错误发生: {e}")

    # 打开图片并进行目标检测
    def open_img(self):
        file_path, _ = QFileDialog.getOpenFileName(None, '打开图片', './', "Image files (*.jpg *.jpeg *.png)")
        if not file_path:
            return

        # 保存图片路径
        self.org_path = file_path
        # self.ui.PiclineEdit.setText(self.org_path)  # 显示图片路径

        # # 读取图片
        # self.org_img = tools.img_cvread(self.org_path)

        # 目标检测
        t1 = time.time()
        self.results = self.model(file_path)[0]  # 假设返回的是一个包含检测结果的对象
        t2 = time.time()
        take_time_str = '{:.3f} s'.format(t2 - t1)
        self.time_label.setText(take_time_str)  # 显示检测时间

        # 获取检测框信息
        location_list = self.results.boxes.xyxy.tolist() if self.results.boxes is not None else []
        self.location_list = [list(map(int, e)) for e in location_list] if location_list else []

        cls_list = self.results.boxes.cls.tolist() if self.results.boxes is not None else []
        self.cls_list = [int(i) for i in cls_list] if cls_list else []

        conf_list = self.results.boxes.conf.tolist() if self.results.boxes is not None else []
        self.conf_list = ['%.2f %%' % (each * 100) for each in conf_list] if conf_list else []

        now_img = self.results.plot()
        # 获取缩放后的图片尺寸
        img_width, img_height = self.get_resize_size(now_img)
        resize_cvimg = cv2.resize(now_img, (img_width, img_height))

        # 将图片转换为 QPixmap 并显示
        pix_img = self.cvimg_to_qpiximg(resize_cvimg)
        self.img_label.setPixmap(pix_img)
        self.img_label.setAlignment(Qt.AlignCenter)

        # 更新目标检测结果
        self.update_results()

    # 打开视频进行识别
    def open_video(self):
        try:
            self.restults_table.setRowCount(0)  # 清空表格
            self.comboBox.clear()  # 清空目标选择下拉框
            self.name_label.clear()  # 清空类别
            self.con_label.clear()
            self.num_label.clear()
            self.time_label.clear()
            file_path, _ = QFileDialog.getOpenFileName(None, '打开视频', './', "Video files (*.mp4 *.avi *.mov)")
            if not file_path:
                return

            # 保存视频路径
            self.org_path = file_path

            # 打开视频文件
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                print("无法打开视频")
                return

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # 进行目标检测
                t1 = time.time()
                self.results = self.model(frame)[0]
                t2 = time.time()
                take_time_str = '{:.3f} s'.format(t2 - t1)
                self.time_label.setText(take_time_str)  # 显示检测时间

                # 获取检测框信息
                location_list = self.results.boxes.xyxy.tolist() if self.results.boxes is not None else []
                self.location_list = [list(map(int, e)) for e in location_list] if location_list else []

                cls_list = self.results.boxes.cls.tolist() if self.results.boxes is not None else []
                self.cls_list = [int(i) for i in cls_list] if cls_list else []

                conf_list = self.results.boxes.conf.tolist() if self.results.boxes is not None else []
                self.conf_list = ['%.2f %%' % (each * 100) for each in conf_list] if conf_list else []

                now_img = self.results.plot()

                # 获取缩放后的图像尺寸
                img_width, img_height = self.get_resize_size(now_img)
                resize_cvimg = cv2.resize(now_img, (img_width, img_height))

                # 将图像转换为QPixmap并显示
                pix_img = self.cvimg_to_qpiximg(resize_cvimg)
                self.img_label.setPixmap(pix_img)
                self.img_label.setAlignment(Qt.AlignCenter)

                # 在此可以加入延时，以便视频正常播放
                cv2.waitKey(30)  # 30毫秒延时，调整视频帧速率

                # 更新目标检测结果
                self.update_results()

            cap.release()  # 释放视频资源
        except Exception as e:
            print(f"错误发生: {e}")

    #打开摄像头
    def open_camera(self):
        try:
            self.restults_table.setRowCount(0)  # 清空表格
            self.comboBox.clear()  # 清空目标选择下拉框
            self.name_label.clear()  # 清空类别
            self.con_label.clear()
            self.num_label.clear()
            self.time_label.clear()

            self.org_path = ''
            # 打开摄像头
            url = 'https://192.168.137.94:8080/video'  # 远程摄像头url地址
            cap = cv2.VideoCapture(url)  # 0表示默认摄像头，若有多个摄像头可改为1, 2等，这里使用手机摄像头
            if not cap.isOpened():
                print("无法打开摄像头")
                return

            while True:
                ret, frame = cap.read()  # 读取摄像头帧
                if not ret:
                    print("无法读取摄像头帧")
                    break

                # 进行目标检测
                t1 = time.time()
                self.results = self.model(frame)[0]
                t2 = time.time()
                take_time_str = '{:.3f} s'.format(t2 - t1)
                self.time_label.setText(take_time_str)  # 显示检测时间

                # 获取检测框信息
                location_list = self.results.boxes.xyxy.tolist() if self.results.boxes is not None else []
                self.location_list = [list(map(int, e)) for e in location_list] if location_list else []

                cls_list = self.results.boxes.cls.tolist() if self.results.boxes is not None else []
                self.cls_list = [int(i) for i in cls_list] if cls_list else []

                conf_list = self.results.boxes.conf.tolist() if self.results.boxes is not None else []
                self.conf_list = ['%.2f %%' % (each * 100) for each in conf_list] if conf_list else []

                # 目标检测结果绘制
                now_img = self.results.plot()

                # 获取缩放后的图像尺寸
                img_width, img_height = self.get_resize_size(now_img)
                resize_cvimg = cv2.resize(now_img, (img_width, img_height))

                # 将图像转换为QPixmap并显示
                pix_img = self.cvimg_to_qpiximg(resize_cvimg)
                self.img_label.setPixmap(pix_img)
                self.img_label.setAlignment(Qt.AlignCenter)

                # 更新目标检测结果
                self.update_results()

                # 在此可以加入延时，以便视频正常播放
                cv2.waitKey(1)  # 1毫秒延时，以确保视频流实时更新

            cap.release()  # 释放摄像头资源
        except Exception as e:
            print(f"打开摄像头时发生错误: {e}")

    # 更新UI显示检测结果
    def update_results(self):
        org_path = self.org_path
        location_list = self.location_list
        cls_list = self.cls_list
        conf_list = self.conf_list

        # 如果没有检测结果，显示提示信息并清空UI
        if not location_list:
            self.num_label.setText("0")  # 更新检测到的目标数目
            self.restults_table.setRowCount(0)  # 清空表格
            self.comboBox.clear()  # 清空目标选择下拉框
            self.comboBox.addItem("无检测结果")  # 提示无检测结果
            self.name_label.setText("无")  # 清空类别
            self.con_label.setText("无")  # 清空置信度
            return

        # 获取当前表格中已有的行数
        current_row_count = self.restults_table.rowCount()

        # 设置表格的行数，增加当前检测结果的行数
        self.restults_table.setRowCount(current_row_count + len(location_list))

        # 填充新检测结果到表格中
        for row in range(len(location_list)):
            # 序号
            self.restults_table.setItem(current_row_count + row, 0, QTableWidgetItem(str(current_row_count + row + 1)))
            # 文件路径
            self.restults_table.setItem(current_row_count + row, 1, QTableWidgetItem(org_path))
            # 类别
            self.restults_table.setItem(current_row_count + row, 2, QTableWidgetItem(plant_list[cls_list[row]]))
            # 置信度
            self.restults_table.setItem(current_row_count + row, 3, QTableWidgetItem(str(conf_list[row])))
            # 位置
            location_str = f"[{location_list[row][0]}, {location_list[row][1]}, " \
                           f"{location_list[row][2]}, {location_list[row][3]}]"
            self.restults_table.setItem(current_row_count + row, 4, QTableWidgetItem(location_str))

        # 滚动到最后一行
        self.restults_table.scrollToItem(self.restults_table.item(current_row_count + len(location_list) - 1, 0),QAbstractItemView.PositionAtBottom)

    # 更新目标数目
        total_nums = len(location_list)
        self.num_label.setText(str(total_nums))

        # 设置目标选择下拉框
        choose_list = ['全部']
        target_names = [self.results.names[id] + '_' + str(index) for index, id in enumerate(cls_list)]
        choose_list += target_names
        self.comboBox.clear()
        self.comboBox.addItems(choose_list)

        self.name_label.setText(plant_list[cls_list[0]])
        self.con_label.setText(conf_list[0])

        # 设置 QComboBox 的当前索引改变事件
        self.comboBox.currentIndexChanged.connect(self.update_target_info)

    # 目标选择变化时，更新类型和置信度
    def update_target_info(self):
        # 获取QComboBox中选中的目标索引
        selected_index = self.comboBox.currentIndex() - 1

        if selected_index >= 0:  # 如果有选择项
            # 从cls_list和conf_list中获取选中目标的信息


            # 更新类型和置信度标签
            self.name_label.setText(plant_list[self.cls_list[selected_index]])
            self.con_label.setText(self.conf_list[selected_index])

    def get_resize_size(self, img):
        self.show_width = 681
        self.show_height = 421
        _img = img.copy()
        img_height, img_width, depth = _img.shape
        ratio = img_width / img_height
        if ratio >= self.show_width / self.show_height:
            self.img_width = self.show_width
            self.img_height = int(self.img_width / ratio)
        else:
            self.img_height = self.show_height
            self.img_width = int(self.img_height * ratio)
        return self.img_width, self.img_height

    def cvimg_to_qpiximg(self,cvimg):
        """
        将OpenCV图像（BGR格式）转换为QPixmap。
        """
        # 将图像从BGR转换为RGB
        rgb_img = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)

        # 获取图像的尺寸
        h, w, c = rgb_img.shape
        bytes_per_line = c * w  # 每行字节数

        # 创建QImage对象
        qimage = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # 将QImage转换为QPixmap
        pixmap = QPixmap.fromImage(qimage)

        return pixmap




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()                    # ui是Ui_MainWindow()类的实例化对象
    ui.setupUi(MainWindow)                  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())                   # 使用exit()或者点击关闭按钮退出QApplication