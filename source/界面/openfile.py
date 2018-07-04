# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
import sys
#from form import Ui_form   # 导入生成first.py里生成的类
from TensorFlowTest.PM25Process.form import Ui_form
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
import os
from pylab import *
from TensorFlowTest.ImageProcess.Image2Pm import PmAnalyse;

#matplotlib.rcParams['font.sans-serif'] = ['SimHei'];
#matplotlib.rcParams['axes.unicode_minus'] = False;
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号‘-’显示为方块的问题
class mywindow(QtWidgets.QWidget,Ui_form):
    imgData=''
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

        #与pm相关的变量
        self.sizes=None;

        #导入模型
        self.pm=PmAnalyse();

        #定义槽函数
    def openimage(self):
   # 打开文件路径
   #设置文件扩展名过滤,注意用双分号间隔
        imgName,imgType= QFileDialog.getOpenFileName(self,"打开图片",""," *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
        print(imgName)
        #利用qlabel显示图片
        png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(png)
        #显示名字
        name = imgName.split("/")
        self.label_5.setText("("+name[-1]+")")
        self.imgData=imgName
        return imgName
    #这里进行数据分析处理
    def analysisPm25(self):
        print(self.imgData)
        if self.imgData=='':
            reply = QMessageBox.information(self,"警告","请先输入图片数据！",QMessageBox.Ok)
        else:

            #处理图片数据
            self.sizes=self.pm.image2pm25(self.imgData);
            print(self.sizes);
            output=np.argmax(self.sizes);
            print(output)
            #print("dosomething")
            #数据处理完成后得到输出，假设现在得到输出为一个数组
            #output=1
            if output==0:
                self.label_3.setText("优(pm2.5值:0-50)等级0")
            elif output==1:
                self.label_3.setText("良(pm2.5值:50-100)等级1")
            elif output==2:
                self.label_3.setText("轻度污染(pm2.5值:100-150)等级2")
            elif output==3:
                self.label_3.setText("中度污染(pm2.5值:150-200)等级3")
            elif output==4:
                self.label_3.setText("重度污染(pm2.5值:200-250)等级4")
            else:
                self.label_3.setText("严重污染(pm2.5值:>=250)等级5")
    def outputHist(self):
        #输入数据
        #datas=self.sizes;
        #datas=[0.02,0.02,0.7,0.1,0.05,0.1]

        #data = {'优': self.sizes[0], '良': self.sizes[1], '轻度污染': self.sizes[2], '中度污染':self.sizes[3], '重度污染': self.sizes[4], '严重污染': self.sizes[5]}
        data = {'0': self.sizes[0], '1': self.sizes[1], '2': self.sizes[2], '3': self.sizes[3],
                '4': self.sizes[4], '5': self.sizes[5]}

        colors=['lime','yellowgreen','gray','lightskyblue','pink','red']



        plt.figure()  # 新图

        for a, b in data.items():
            plt.text(a, b, '%.2f'%b, ha='center', va='bottom', fontsize=20)

        x_axis = tuple(data.keys())
        y_axis = tuple(data.values())
        x_arr=np.arange(len(x_axis))
        #print(x_arr)

        # print(x_axis)
        # print(type(x_axis))
        plt.xticks(x_arr, x_axis)
        x_axis =('0','1','2','3','4','5')
        # print(x_axis)
        # print(type(x_axis))
        # plt.bar(x_arr, y_axis, color=colors)
        plt.bar(x_axis,y_axis,color=colors)
        plt.xlabel("PM2.5浓度状况",fontsize=15)
        plt.ylabel("估算概率",fontsize=15)
        plt.title("PM2.5浓度识别概率直方图",fontsize=15)
        plt.ylim(0, 1)
        plt.savefig("HistChart.png")
        png = QtGui.QPixmap("HistChart.png").scaled(self.label_4.width(), self.label_4.height())
        self.label_4.setPixmap(png)

    def outputPie(self):
      #try:
        plt.figure(figsize=(6.0,4.38))
        #定义饼状图标签
        labels = [u'优',u'良',u'轻度污染',u'中度污染',u'重度污染',u'严重污染']
        #输入数据
        #sizes = [1,3,6,65,10,15]
        colors = ['red','yellowgreen','lightskyblue','gray','green','pink']
        #将某部分突出
       # explode = (0.3,0.2,0.1,0.0,0.015,0.005)
        #labeldistance,文本的位置离原点有多远，1.1指半径的1.1倍
        #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        #shadow，饼状图是否有阴影
        #startangle，起始角度，0表示从0开始旋转，为第一块。一般选择从90度开始比较好看
        #pctdistance，百分比的text离圆心的距离
        #patches,l_text,p_text,为了得到饼状图的返回值，p_text为饼图内部文本，l_text为饼图外的Label文本
        patches,l_text,p_text = plt.pie(self.sizes,labels=labels,colors=colors,
                                        labeldistance = 1.2,autopct='%3.1f%%',shadow=False,
                                        startangle=90,pctdistance = 0.6)

        #改变文本大小，方法是把每一个text遍历，调用set_size方法设置它的属性
        for t in l_text:
            t.set_size(0)
        for t in p_text:
            t.set_size(10)
        #设置x,y轴刻度一致，这样饼图才是圆的
        plt.axis('equal')
        #plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
        plt.legend()
        plt.savefig("PieChart.png")
        png = QtGui.QPixmap("PieChart.png").scaled(self.label_4.width(), self.label_4.height())
        self.label_4.setPixmap(png)

app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.show()
sys.exit(app.exec_())