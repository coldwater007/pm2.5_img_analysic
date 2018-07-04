# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\100D5300\temp\pyqt01\form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Ui_form(object):
    def setupUi(self, form):
        self.form=form
        form.setObjectName("form")
        self.OrigiHeight=320
        self.ChangeHeight=700
        self.pieChartHeight=700
        #设置背景
       # form.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
       # form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        form.setWindowOpacity(0.98)
        palette1=QPalette()
        palette1.setBrush(self.backgroundRole(),QBrush(QPixmap('imageSrc\\back.jpg')))
        form.setPalette(palette1)
        form.setAutoFillBackground(True)
        form.setGeometry(QRect(500,400,500,self.OrigiHeight))
        form.setWindowIcon(QIcon('imageSrc\\LOGO.png'))
        #form.resize(437, 330)
        #self.machine = QStateMachine()
        self.centralWidget = QtWidgets.QWidget(form)
        self.centralWidget.setObjectName("centralWidget")
        self.chooseImg = QtWidgets.QPushButton(self.centralWidget)
        self.chooseImg.setGeometry(QtCore.QRect(20, 30, 101, 31))
        self.chooseImg.setStyleSheet("gridline-color: rgb(199, 85, 47);")
        self.chooseImg.setObjectName("chooseImg")
        self.chooseImg.setIcon(QIcon('imageSrc\\fileLogo.png'))
        self.Analysis = QtWidgets.QPushButton(self.centralWidget)
        self.Analysis.setGeometry(QtCore.QRect(20, 140, 101, 31))
        self.Analysis.setObjectName("Analysis")
        self.Analysis.setIcon(QIcon('imageSrc\\searchon.png'))
        #self.Analysis.setIcon(QIcon('D:\\100D5300\\sun.png'))
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(30, 230, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(140, 230, 300, 15))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(140, 10, 350, 210))
       # self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.114, y1:0.125, x2:1, y2:1, stop:0 rgba(255, 222, 201, 193), stop:1 rgba(255, 255, 255, 255));")
        #self.label.setStyleSheet("QLabel{background-image:url(back.jpg);}")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(10,340,480,340))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(365,230,220,15))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QIcon('imageSrc\\histLogo.png'))
        #self.pushButton.setStyleSheet('QPushButton{background-image:url(D:\\100D5300\\1.jpg)}')

        self.circle = QtWidgets.QPushButton(self.centralWidget)
        self.circle.setGeometry(QtCore.QRect(150, 260, 101, 31))
        self.circle.setObjectName("circle")
        self.circle.setIcon(QIcon('imageSrc\\pieLogo.png'))
        #form.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(form)
        self.mainToolBar.setObjectName("mainToolBar")
        #form.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(form)
        self.statusBar.setObjectName("statusBar")
        #form.setStatusBar(self.statusBar)

        self.quit = QtWidgets.QPushButton(self.centralWidget)
        self.quit.setGeometry(QtCore.QRect(380, 260, 101, 31))
        self.quit.setObjectName("quit");
        self.quit.setIcon(QIcon('imageSrc\\quit.png'))
        self.mainToolBar=QtWidgets.QToolBar(form);
        #self.connect(quit, QtCore.SIGNAL('clicked()'),

        self.retranslateUi(form)
        self.movie = QtGui.QMovie("imageSrc\\photoInput.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.chooseImg.clicked.connect(form.openimage)
        self.Analysis.clicked.connect(form.analysisPm25)
        self.pushButton.clicked.connect(self.change)
        self.circle.clicked.connect(self.change)
        self.quit.clicked.connect(QCoreApplication.instance().quit);
        #self.circle.clicked.connect(self.showProgress)
        QtCore.QMetaObject.connectSlotsByName(form)
        self.form.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        #self.form.setWindowFlags(QtCore.Qt.CustomizeWindowHint);

    def change(self):
        CurrentHeight = self.height()
        if self.OrigiHeight==CurrentHeight:
            startHeight = self.OrigiHeight
            endHeight = self.ChangeHeight
            if self.sender().text() == '直方图︾':
                #self.label_4.setGeometry(QtCore.QRect(10, 340, 480, 340))
               try:
                self.form.outputHist()

               except:
                   reply = QMessageBox.information(self, "警告", "请先进行分析！", QMessageBox.Ok)
                   return;
               self.pushButton.setText(u'直方图︽')
               self.circle.setEnabled(False)
            elif self.sender().text() == '饼状图︾':
               # self.label_4.setGeometry(QtCore.QRect(10, 340, 480, 340))
               try:
                endHeight = self.pieChartHeight
                self.form.outputPie()
                self.circle.setText(u'饼状图︽')
                self.pushButton.setEnabled(False)
               except:
                   reply = QMessageBox.information(self, "警告", "请先进行分析！", QMessageBox.Ok)
                   return;
        else:
            startHeight = self.ChangeHeight
            endHeight = self.OrigiHeight
            if self.sender().text() == '直方图︽':
                self.circle.setEnabled(True)
                self.pushButton.setText(u'直方图︾')
            elif self.sender().text() == '饼状图︽':
                self.pushButton.setEnabled(True)
                startHeight=self.pieChartHeight
                self.circle.setText(u'饼状图︾')
        self.animation = QPropertyAnimation(self,b'geometry')
        self.animation.setDuration(800)
        #+9,+38是因为每次窗口都会上移，用来使窗口固定
        self.animation.setStartValue(QRect(self.x()+9,self.y()+38,500,startHeight))
        self.animation.setEndValue(QRect(self.x()+9,self.y()+38,500,endHeight))
        self.animation.start()


    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "PM2.5图片分析估计系统"))
        self.chooseImg.setText(_translate("form", "选择照片"))
        self.Analysis.setText(_translate("form", "开始分析"))
        self.label_4.setText(_translate("form","暂无数据，请先输入数据"))
        self.label_2.setText(_translate("form", "分析结果："))
        self.label_3.setText(_translate("form", "(PM2.5污染情况)"))
        self.label_5.setText(_translate("form",""))
        self.label.setText(_translate("form", "………………照片在此显示………………"))
        self.pushButton.setText(_translate("form", "直方图︾"))
        self.circle.setText(_translate("form", "饼状图︾"))
        self.quit.setText(_translate("form", "退出"))
        self.mainToolBar.setWindowTitle(_translate("form", "PM2.5分析系统"));



