from sklearn.naive_bayes import GaussianNB
import numpy as np;
import TensorFlowTest.KerasTest.LoadData as ld;
import tensorflow as tf
if __name__=="__main__":
    # docData, docLabel = ld.LoadData();
    # np.savez("docData.npz")
    # trainData, trainLabel, testData, testLabel = ld.getTrainAndTest(docData, docLabel);

    train = np.load("trainData.npz");
    trainData = train["trainData"];
    trainLabel = train["trainLabel"];
    test = np.load("testData.npz");
    testData = test["testData"];
    testLabel = test["testLabel"]

    trainData = np.array(trainData);
    testData = np.array(testData);
    gl=GaussianNB();
    gl.fit(trainData,trainLabel);
    predict_gl=gl.predict(testData);
    print(predict_gl);
    print(testLabel)
    count=0;
    for i in range(len(predict_gl)):
        if predict_gl[i]==testLabel[i]:
            count+=1;
    result=float(count)/float(len(predict_gl));
    print("准确率:"+str(result));


    # if 'session' in locals() and session is not None:
    #     print('Close interactive session')
    #     session.close()