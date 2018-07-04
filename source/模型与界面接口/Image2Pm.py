#-*- coding:utf-8 -*-
from keras.utils.np_utils import to_categorical
from keras.models import load_model
import numpy as np;
import TensorFlowTest.ImageProcess.PM25Test as pm
import matplotlib.pyplot as plt
import matplotlib


class PmAnalyse():
    model=None;
    def __init__(self):
        self.model = load_model("pm_model.h5")


    def project1_test(self,testData):
        testData = np.array(testData);
        result = self.model.predict(testData);
        return result;

    # 由图像转为与pm2.5相关的tx
    def image2tx(self,imageName):
        tx = pm.getTx_test(imageName);
        return tx;

    def image2pm25(self,imageName):
        tx = self.image2tx(imageName);
        result=self.project1_test([tx]);
        #self.paint(np.array(result).flatten());
        return np.array(result).flatten();

    def image2pm25_2(self,testData,testLabel):
        categorical_test_labels = to_categorical(testLabel, num_classes=None)
        result=self.model.evaluate(testData,categorical_test_labels,batch_size=2);
        predic=self.model.predict(testData);
        return result,predic;

    def paint(self,his):
        #print();
        matplotlib.rcParams['font.sans-serif'] = ['SimHei'];
        matplotlib.rcParams['axes.unicode_minus'] = False;
        # label_list = [str(i) for i in range(6)];    # 各部分标签
        #label_list = ["优", "良", "轻度污染", "中度污染", "重度污染", "严重污染"]
        label_list=["轻度污染","中度污染","严重污染","良","严重污染","优"]
        color = ["lime", "green", "yellow","blue", "m", "red"]  # 各部分颜色
        patches, l_text, p_text = plt.pie(his, colors=color, labels=label_list, labeldistance=1.1, autopct="%1.1f%%",
                                          shadow=False, startangle=90, pctdistance=0.6)
        plt.axis("equal")  # 设置横轴和纵轴大小相等，这样饼才是圆的
        plt.legend()
        plt.show()

if __name__=="__main__":
    pmtest = PmAnalyse();

    # image="performance/白.jpg";
    # pre=pmtest.image2pm25(image);
    # print(np.argmax(pre));
    #
    # image = "performance/84.5.jpg";
    # pre=pmtest.image2pm25(image);
    # print(np.argmax(pre));
    #
    # image = "performance/134.5.jpg";
    # pre=pmtest.image2pm25(image);
    # print(np.argmax(pre));

    test=np.load("testData.npz");
    testData=test["testData"];
    testLabel=test["testLabel"];
    result,predic=pmtest.image2pm25_2(testData,testLabel);
    print("预测:",np.argmax(predic,1))
    print("准确率",result[1]);
