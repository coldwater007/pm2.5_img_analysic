#-*- coding:utf-8 -*-
from PIL import Image
import os
import pymysql
import re

def get_imgTime(path_):
    files = os.listdir(path_)
    print(files)
    for each_imgname in files:
        each_img = re.split('201', each_imgname)
        change = each_img[1].split('-')
        if (len(change[1]) == 1):
            change[1] = '0' + change[1]
        if (len(change[2]) == 5):
            change[2] = '0' + change[2]
        change_time = '201' + change[0] + '-' + change[1] + '-' + change[2]
        theTime=change_time.split('.')
        print(theTime[0])
        sql = "select PM25 from pm25data.pm_data where city='上海' and each_time='" + theTime[0] + "'"
        cursor.execute(sql)
        pm_25 = cursor.fetchall()
        try:
           pm_25 = pm_25[0][0]
        except:
            continue
        print(pm_25)
        file = ''
        if pm_25 >= 0 and pm_25 < 50:
            file = '0\\'
        elif pm_25 >= 50 and pm_25 < 70:
            file = '1\\'
        elif pm_25 >= 70 and pm_25 < 90:
            file = '2\\'
        elif pm_25 >= 90 and pm_25 < 110:
            file = '3\\'
        elif pm_25 >= 110 and pm_25 < 150:
            file = '4\\'
        elif pm_25 >= 150 and pm_25 < 200:
            file = '5\\'
        elif pm_25 >= 200 and pm_25 < 250:
            file = '6\\'
        else:
            file = '7\\'
        img = Image.open(path_+'\\'+each_imgname)
        final_path=local+file+each_img[0]+theTime[0]+'.jpg'
        img.save(final_path)

if __name__=='__main__':
    path_="F:\\Data\\shanghai"
    get_imgTime(path_)