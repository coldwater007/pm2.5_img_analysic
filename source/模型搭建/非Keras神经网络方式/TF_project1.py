#-*- coding:utf-8 -*-
import tensorflow as tf;
import numpy as np;
import TensorFlowTest.KerasTest.LoadData as ld;

#docData,docLabel=ld.LoadData();

#将样本标签转换成独热编码
def label_change(before_label):
    label_num=len(before_label)
    change_arr=np.zeros((label_num,8))
    for i in range(label_num):
        #该样本标签原本为0-32的，本人疏忽下32标记成33
        change_arr[i, int(before_label[i])] = 1
    return change_arr

INPUT_NODE=400;
OUTPUT_NODE=8;
BATCH_SIZE=40;
LAYER1_NODE=50;

#定义学习率，学习率衰减速度，正则系数，训练调整参数的次数以及平滑衰减率
LEARNING_RATE_BASE=0.5
LEARNING_RATE_DECAY=0.99
REGULARIZATION_RATE=0.0001  #?????????????
TRAINING_STEPS=4000
MOVING_AVERAGE_DECAY=0.99

#定义整个神经网络的结构，也就是向前传播的过程，avg_class为平滑可训练量的类，不传入则不使用平滑
def inference(input_tensor,avg_class,w1,b1,w2,b2):
    if avg_class==None:
        #第一层隐含层，输入与权重矩阵乘后加上常数传入激活函数作为输出
        layer1=tf.nn.relu(tf.matmul(input_tensor,w1)+b1)
        #第二层隐含层，前一层的输出与权重矩阵乘后加上常数作为输出
        #layer2=tf.nn.relu(tf.matmul(layer1,w2)+b2)
        #返回 第二层隐含层与权重矩阵乘加上常数作为输出
        return tf.matmul(layer1,w2)+b2
    else:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, avg_class.average(w1)) + avg_class.average(b1))
        #layer2 = tf.nn.relu(tf.matmul(layer1, avg_class.average(w2)) + avg_class.average(b2))
        return tf.matmul(layer1, avg_class.average(w2)) + avg_class.average(b2)

def train():
    # trainData,trainLabel,testData,testLabel=ld.getTrainAndTest(docData,docLabel);
    # np.savez("trainfile.npz",trainData=trainData,trainLabel=trainLabel);
    # np.savez("testfile.npz",testData=testData,testLabel=testLabel);
    # docData = np.load("docDataFile.npy");
    # docLabel = np.load("docLabelFile.npy");
    # trainData, trainLabel, testData, testLabel = ld.getTrainAndTest(docData, docLabel);
    train=np.load("trainData.npz");
    trainData=train['trainData'];trainLabel=train['trainLabel'];
    test=np.load("testData.npz");
    testData=test['testData'];testLabel=test['testLabel'];



    # 定义输出数据的地方，None表示无规定一次输入多少训练样本,y_是样本标签存放的地方
    x = tf.placeholder(tf.float32, shape=[None, INPUT_NODE], name='x-input')
    y = tf.placeholder(tf.float32, shape=[None, OUTPUT_NODE], name='y-input')
    print(np.array(x).shape);
    #定义权重和bias
    # 依次定义每一层与上一层的权重，这里用随机数初始化，注意shape的对应关系
    w1 = tf.Variable(tf.truncated_normal(shape=[INPUT_NODE, LAYER1_NODE], stddev=0.1));
    b1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]));

    w2=tf.Variable(tf.truncated_normal(shape=[LAYER1_NODE,OUTPUT_NODE],stddev=0.1));
    b2=tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]));

    y=inference(x,None,w1,b1,w2,b2);
    # 每训练完一次就会增加的变量 trainable表示是否需要优化
    global_step = tf.Variable(0, trainable=False);

    # 定义平滑变量的类，输入为平滑衰减率和global_step使得每训练完一次就会使用平滑过程
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    # 将平滑应用到所有可训练的变量，即trainable=True的变量
    variable_averages_op = variable_averages.apply(tf.trainable_variables())

    # 输出平滑后的预测值
    average_y = inference(x, variable_averages, w1, b1, w2, b2)

    # 定义交叉熵和损失函数，但为什么传入的是label的arg_max(),就是对应分类的下标呢，我们迟点再说
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y, 1))         #?????????????????????????
    # 计算交叉熵的平均值，也就是本轮训练对所有训练样本的平均值
    cross_entrip_mean = tf.reduce_mean(cross_entropy)

    # 定义正则化权重，并将其加上交叉熵作为损失函数
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE);
    regularization = regularizer(w1) + regularizer(w2);
    loss = cross_entrip_mean + regularization

    # 定义动态学习率，随着训练的步骤增加不断递减
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, 900, LEARNING_RATE_DECAY)
    # 定义向后传播的算法，梯度下降发，注意后面的minimize要传入global_step
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    # 管理需要更新的变量，传入的参数是包含需要训练的变量的过程
    train_op = tf.group(train_step, variable_averages_op)
    #train_op=tf.group(train_step);

    #正确率预测
    correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        init_op=tf.global_variables_initializer();
        sess.run(init_op);

        print(np.array(testLabel).shape);
        train_size=np.array(testLabel).shape[0];
        new_trainLabel=label_change(trainLabel);
        new_testLabel=label_change(testLabel);
        print(np.array(new_testLabel).shape);
        print(np.array(new_trainLabel).shape);

        #train_feed={x:trainData,y:new_trainLabel};
        test_feed={x:testData,y:new_testLabel};
        for i in range(TRAINING_STEPS):
            start=(i*BATCH_SIZE)%train_size;
            end=min(start+BATCH_SIZE,train_size);
            #print(np.array(trainData[start:end]).shape);
            train_feed = {x: trainData[start:end], y: new_trainLabel[start:end]};
            if i%100==0:
                validate_acc = sess.run(accuracy, feed_dict=train_feed)
                print("After %d training step(s),validation accuracy using average model is %g" % (i, validate_acc))
            # 每一轮通过同一训练集训练
            sess.run(train_op, feed_dict=train_feed)

        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print("After %d training step(s),test accuracy using average model is %g" % (TRAINING_STEPS, test_acc))

if __name__=="__main__":
    train();

