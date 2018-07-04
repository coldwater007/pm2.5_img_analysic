#-*- coding:utf-8 -*-
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
import TensorFlowTest.KerasTest.PM25Test as pm
import numpy as np
from sklearn.svm import SVR;
from sklearn.multiclass import OneVsRestClassifier
from keras.utils.np_utils import to_categorical
import TensorFlowTest.KerasTest.LoadData as ld;


#构建神经网络
# model=Sequential();
# model.add(Dense( 200, input_dim=90000,activation='relu'))
# model.add(Dense( 100, activation='relu'))
# model.add(Dense(10, activation='softmax'))
#
# #model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")
# model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])
# List = ["30.jpg", "47.5.jpg", "52.5.jpg", "56.5.jpg", "60.5.jpg", "66.jpg", "71.jpg", "74.jpg", "80.5.jpg",
#                 "88.jpg", "91.jpg", "98.5.jpg", "131.jpg", "135.jpg",
#                 "152.jpg", "164.5.jpg", "238.jpg", "244.jpg", "256.5.jpg"];
# TrainSet = np.array(pm.TrainData(List));
# print(len(TrainSet[0]))
# TrainOutput = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9]
# categorical_labels = to_categorical(TrainOutput, num_classes=None)
#
# model.fit(TrainSet,categorical_labels, epochs=80, batch_size=5);
#test_tx=pm.getTx("135.jpg");
#Class=model.predict(np.mat(test_tx));
#print(Class);
#print(test_tx);
#print(model.predict(test_tx));

def NeuralNet(trainData,trainLabel,testData,testLabel):
    #构建神经网络
    model = Sequential();
    model.add(Dense(200, input_dim=400, activation='relu'))
    #model.add(Dropout(0.5));
    model.add(Dense(100, activation='relu'))
    #model.add(Dropout(0.5));
    model.add(Dense(80, activation='relu'))
    # model.add(Dropout(0.5));
    model.add(Dense(50, activation='relu'))
    # model.add(Dropout(0.5));
    #model.add(Dense(30, activation='relu'))
    # model.add(Dropout(0.5));
    model.add(Dense(6, activation='softmax'))

    # model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")
    model.compile(loss='categorical_crossentropy', optimizer='Adagrad', metrics=['accuracy'])
    categorical_train_labels = to_categorical(trainLabel, num_classes=None)
    model.fit(trainData, categorical_train_labels, epochs=370, batch_size=100);

    categorical_test_labels = to_categorical(testLabel, num_classes=None)

    #result=model.predict(testData,testLabel);

    result=model.evaluate(testData,categorical_test_labels,batch_size=2);
    #print(testData[0]);
    res=model.predict(testData);
    print(res[0]);
    print(np.argmax(res[0]));
    print("准确率:"+str(result));

    #model.save("pm_model.h5");



if __name__=="__main__":
    # docData,docLabel=ld.LoadData();
    # print(docData)
    # print(docLabel);
    # np.save("docDataFile.npy",docData);
    # np.save("docLabelFile.npy",docLabel);
    # docData=np.load("docDataFile.npy");
    # docLabel=np.load("docLabelFile.npy");
    # # # #将训练数据和测试数据放入文件中
    #trainData,trainLabel,testData,testLabel=ld.getTrainAndTest(docData,docLabel);
    #print(type(testData))
    #print(testData[0])
    # np.savez("trainData.npz",trainData=trainData,trainLabel=trainLabel);
    # np.savez("testData.npz",testData=testData,testLabel=testLabel);

    train=np.load("trainData.npz");
    trainData=train["trainData"];
    trainLabel=train["trainLabel"];
    test=np.load("testData.npz");
    testData=test["testData"];
    testLabel=test["testLabel"];
    trainData=np.array(trainData);
    # print(trainData.shape)
    testData=np.array(testData);
    # print(testData.shape)
    # print(np.shape([testData[0]]))
    #docData=np.array(docData);

    #svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1);
    #result = OneVsRestClassifier(svr_rbf, -1).fit(trainData, trainLabel).score(testData, testLabel)
    #print("准确率:"+str(result));

    #神经网络的方法
    NeuralNet(trainData,trainLabel,testData,testLabel);