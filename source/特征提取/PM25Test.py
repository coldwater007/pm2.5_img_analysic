import cv2
import numpy as np


'''
def zmMinFilterGray(src, r=7):
    最小值滤波，r是滤波器半径
    if r <= 0:
        return src
    #print(src.shape)
    #print(src.shape[:2])
    h, w = src.shape[:2]
    print(h,w);
    I = src
    print(list(range(1, h)) + [h - 1]);
    #print(np.array(I[[0] + list(range(h - 1)),:]).shape);
    res = np.minimum(I, I[[0] + list(range(h - 1)), :])
    #print(list(range(1, h)) + [h - 1]);
    res = np.minimum(res, I[list(range(1, h)) + [h - 1], :])
    I = res
    res = np.minimum(I, I[:, [0] + list(range(w - 1))])
    res = np.minimum(res, I[:, list(range(1, w)) + [w - 1]])
    return zmMinFilterGray(res, r - 1)
'''
#h,w为左上角像素的坐标,src
def minLvBoVec(src,rh,rw,h,w):
    #mat = src[h:h + 2 * r + 1, w:w + 2 * r + 1];
    mat=src[h:h + rh, w:w + rw];
    #print(mat*255)
    value = np.mat(mat).min();
    #new_mat = np.ones((2 * r + 1, 2 * r + 1))
    new_mat=np.ones((rh, rw))
    new_mat =new_mat*value;
    #f=open("doc.txt",'w');
    #f.write(str(value)+'\n');
    #print(value*255);
    return new_mat;

def zmMinFilterGray(src, r=7):

    #height,width=src.shape;

    #minVec=np.zeros(height,width);
    #最小滤波器做法1
    #minVec=src;
   # w=int(r/2);
    #1.中间进行最小值滤波
    '''
    for i in range(w,height-w):
        for j in range(w,width-w):
            mats=src[i-w:i+w+1,j-w:j+w+1];
            print(mats*255)
            value=np.mat(mats).min()
            minVec[i][j]=value;
            print(i,j,value*255);
    return minVec;
    '''
    '''
    height, width = src.shape;
    minVec = src;
    #非边缘位置
    hh,ww=int(height/r),int(width/r);
    for i in range(hh-1):
        for j in range(ww-1):
            h=i*r;w=j*r;
            mat=minLvBoVec(src,r,r,h,w);
            minVec[h:h + r, w:w + r] = mat;
            #minVec[h:h+2*r+1,w:w+2*r+1]=mat;

    #最下面的一行(不包含右下角)
    for j in range(ww-1):
        h=(hh-1)*r;w=j*r;
        new_r=(height-h);
        mat = minLvBoVec(src,new_r,r,h,w);
        minVec[h:height, w:w + r] = mat

    #最右边一列(不包含右下角)
    for i in range(hh-1):
        h=i*r;w=(ww-1)*r;
        new_r=width-w;
        mat = minLvBoVec(src,r,new_r, h, w);
        minVec[h:h + r,w:width] = mat;

    #最右下角 h=height-(hh-1)*r;w=width-ww-1)*r;
    h=(hh-1)*r;w=(ww-1)*r;
    rh=height-h;rd=width-w;
    mat=minLvBoVec(src,rh,rd,h,w);
    minVec[h:height,w:width]=mat;
    return minVec;
    '''
    return cv2.erode(src, np.ones((r, r)))

#窗口半径,p为误差校验值
def guidedfilter(I, p, r, eps):
    '''''引导滤波，直接参考网上的matlab代码'''
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I        #

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    #print(m_a)
    return m_a * I + m_b

def getV1(m, r, eps,w, maxV1):  # 输入rgb图像，值范围[0,1]
    '''计算大气遮罩图像V1和光照值A, V1 = 1-t/A'''
    Vc = np.min(m, 2)  # 得到暗通道图像
    #cv2.imwrite("E:\\testIMG\\testPython\\gray_img.jpg", Vc*255)

    Vc_min=zmMinFilterGray(Vc, 5)  #最小值滤波后
    #cv2.imwrite("E:\\testIMG\\testPython\\min_img.jpg", Vc_min * 255)
    V1 = guidedfilter(Vc, Vc_min, r, eps)  # 使用引导滤波优化
    #cv2.imwrite("E:\\testIMG\\testPython\\guide_img.jpg", V1 * 255)

    V1=np.clip(V1,0.0,1.0);

    bins = 2000;                 #原来为2000份
    ht = np.histogram(Vc, bins)  # 计算大气光照A  统计函数,分成1000份进行统计
    d = np.cumsum(ht[0]) / float(V1.size)   #d中d[i]为ht[0]前i项之和
    #从后往前进行统计
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    try:
        #print( np.mean(m, 2)[V1 >= ht[1][lmax]])
        A = np.mean(m, 2)[V1 >= ht[1][lmax]].max()  #大于前0.1%中取最大值
    except:
        A=0.95;
    return V1, A

def deHaze(m, r=100, eps=0.05, w=0.90, maxV1=0.80, bGamma=False):
    Vc = np.min(m, 2)  # 得到暗通道图像
    Vv=Vc*255;
    Y = np.zeros(m.shape)
    Yc=np.zeros(m.shape)
    V1, A = getV1(m, r, eps,w, maxV1)  # 得到暗通道图像和大气光照

    tx=1-w*(V1/A);
    #print(tx.shape)
    #tx=guidedfilter(Vc,tx,r,eps);
    #tx1=1-w*(Vc/A);
    #cv2.imwrite("E:\\testIMG\\testPython\\transmissiontx.jpg",tx*255);
    #cv2.imwrite("E:\\testIMG\\testPython\\transmissiontx1.jpg", tx1 * 255);

    t0=np.ones(tx.shape);
    t0=t0*0.1;
    tx = np.maximum(tx, t0);


    '''
    for k in range(3):
        #Yc[:, :, k] = (m[:, :, k] - V1) / (1 - Vc / A)  # 颜色校正
        Y[:,:,k]=(m[:,:,k]-A)/np.maximum(tx,t0)+A;      #恢复公式
        Yc[:, :, k] = (m[:, :, k] - A) / np.maximum(tx1, t0) + A;  # 恢复公式

    Y = np.clip(Y, 0.0, 1.0)        #将Y的元素的值限制在0,1
    Yc=np.clip(Yc,0.0,1.0);
    if bGamma:
        Y = Y ** (np.log(0.5) / np.log(Y.mean()))  # gamma校正,默认不进行该操作
    '''

    #print(tx.flatten());

    return tx.flatten();

#基于cv实现图像缩放
def ResizeImage(OringinImage):

    try:
       newSize=(20,20);  #图像缩放后同一为300*300
       #h,w=OringinImage.shape;
       newImage=cv2.resize(OringinImage,newSize,cv2.INTER_LINEAR);
       return newImage;
    except cv2.error as e:
        raise RuntimeError("OriginImage None");

def TrainData(List):
    TrainSet=[];#newSize=(300,300);
    for item in List:
        #提取图片，并将图像缩放到统一的像素
        init_image=cv2.imread("image/"+item);
        newImage = ResizeImage(init_image);
        tx=deHaze(newImage/255.0);
        TrainSet.append(tx);

    return TrainSet;

def getTx(Image):
    #mat=cv2.imread("Data1/image0/(1).jpg");
    #print(mat);
    #try:
        tx=deHaze(ResizeImage(cv2.imread("Data1/"+Image))/255.0);
        tx=tx.flatten();
        #tx=np.sort(tx)[:300];
        #print(Image,tx);
        #tx=tx*255;
        #image=ResizeImage(cv2.imread("Data1/"+Image));
        #tx=np.min(image,2);
        return tx;
        #return tx.flatten();
   # except:
    #    raise "Error";
#为测试集创建的tx,直接读取文件路径
def getTx_test(image):
    tx=deHaze(ResizeImage(cv2.imread(image))/255.0);
    tx=tx.flatten();
    return tx;

def TestSet():
    List=[1,1,3,5]
    return List;
def getSize():
    return 300*300;
if __name__ == '__main__':
    List=["30.jpg","52.5.jpg","54.jpg","54.5.jpg","56.jpg","56.5.jpg","98.5.jpg","164.5.jpg","256.5.jpg"];
    trainSet=TrainData(List);
    print(len(trainSet));
    mat=cv2.imread('image/54.5.jpg');
    cv2.COLOR_RGB2GRAY
    #mat=cv2.imread('image/54.5.jpg');
    #array=np.array(mat);
    #cv2.imwrite("E:\\testIMG\\testPython\\img.jpg",mat)

    #V1,Vc = deHaze(cv2.imread('image/54.5.jpg') / 255.0);
    #cv2.imwrite("E:\\testIMG\\testPython\\img_result_guider.jpg", V1*255)
    #cv2.imwrite("E:\\testIMG\\testPython\\img_result.jpg", Vc*255)
