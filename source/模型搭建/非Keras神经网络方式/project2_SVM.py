import TensorFlowTest.KerasTest.LoadData as ld
import numpy as np;
from sklearn.svm import SVR
from sklearn.multiclass import OneVsRestClassifier
if __name__=="__main__":
    # docData,docLabel=ld.LoadData();
    # trainData,trainLabel,testData,testLabel=ld.getTrainAndTest(docData,docLabel);
    #
    # np.savez("trainData.npz",trainData=trainData,trainLabel=trainLabel);
    # np.savez("testData.npz",testData=testData,testLabel=testLabel);
    # trainData=np.array(trainData);
    # testData=np.array(testData);
    #docData=np.array(docData);


    train = np.load("trainData.npz");
    trainData = train["trainData"];
    trainLabel = train["trainLabel"];
    test = np.load("testData.npz");
    testData = test["testData"];
    testLabel = test["testLabel"]

    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1);
    result = OneVsRestClassifier(svr_rbf, -1).fit(trainData, trainLabel).score(testData, testLabel)
    print("准确率:"+str(result));