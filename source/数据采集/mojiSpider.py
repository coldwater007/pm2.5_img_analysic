#-*- coding:utf-8 -*-
from urllib.request import urlretrieve
import urllib.parse
import urllib3
import requests
import http.cookiejar
from lxml import etree
from bs4 import BeautifulSoup
import pymysql
import os
import re


conn = pymysql.connect(host='localhost',user='root',passwd='w904403',db='pm25data',port=3306,charset='utf8')
cursor = conn.cursor()
#图片储存路径
local="D:\\100D5300\\"
# 各城市的href
city_href={}
# 各城市的名称
city_name={}

UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

citys_url=['https://tianqi.moji.com/liveview/china/henan']
ee=['郑州']
#得到各城市信息
def getCitys(city_url):
    #city_url="https://tianqi.moji.com/liveview/china/chongqing"
    city_header={ 'User-Agent':UserAgent}
    city_req = urllib.request.Request(city_url, None, city_header)
    city_response = urllib.request.urlopen(city_req)
    city_page = city_response.read().decode('utf-8')
    tree = etree.HTML(city_page)
    for one in tree.xpath('//div[@class="city_hot"]'):
        city_href= one.xpath('.//li//a/@href')
        city_name= one.xpath('.//li//a/text()')
    print(len(city_href))
    return city_href,city_name

#得到图片的拍摄时间和地点信息
def get_imgMessage(ID,citynum):
    header_ = {'User-Agent':UserAgent }
    files = os.listdir('D:\\100D5300\\temp')
    for i in ID:
        # 每张图片的url，从中找到拍摄时间和地点
        img_url = 'https://tianqi.moji.com/liveview/picture/' + ID[i]
        req_ = urllib.request.Request(img_url, None, header_)
        response_ = urllib.request.urlopen(req_)
        the_page_ = response_.read().decode('utf-8')
        soup_ = BeautifulSoup(the_page_, "html.parser")
        # 找到拍摄时间
        img_date = soup_.find_all(id='picture_info_date')
        # 找到拍摄地点
        img_place = soup_.find_all(id='picture_info_addr')
        try:
            img_dateMess = img_date[0].get_text().split(' ')
        except:
            continue
        aroundTime = img_dateMess[1].split(':')
        # 根据拍摄时间对图片进行过滤
        hour_time = aroundTime[0].split('M')
        theImg = soup_.find_all('div', class_='scenery_image_detail')
        # 选择拍摄时间在上午七点到下午五点之间的
        if ((hour_time[0] == 'A' and int(hour_time[1]) >= 9) or (hour_time[0] == 'P' and int(hour_time[1]) <= 4)):
            # 时间段
            #print('时间：'+aroundTime[0])
            # 年-月-日
            #print('年月日：'+img_dateMess[0])
            '''
               以下是重要函数
            '''

            # 图片url
            for Img in theImg:
                link = Img.find('img')['src']

                #将时间字符串转为标准格式
                tempList=img_dateMess[0].split('-')
                if len(tempList[1])==1:
                    tempList[1]='0'+tempList[1]
                if len(tempList[2])==1:
                    tempList[2] = '0' + tempList[2]
                img_date = tempList[0]+'-'+tempList[1]+'-'+tempList[2]
                totalname=aroundTime[0]+'#'+city_name[citynum]+img_date+'.jpg'
                for filen in files:
                    if filen==totalname:
                        print(link)
                        print(img_date)
                        # 储存图片
                        sql = "select PM25 from pm25data.pm_data where city='" + ee + "' and each_time='" + img_date + "'"
                        cursor.execute(sql)
                        pm_25 = cursor.fetchall()
                        try:
                            pm_25 = pm_25[0][0]
                        except:
                            continue
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
                        try:
                            urllib.request.urlretrieve(link, local + file + aroundTime[0] + '#' + city_name[
                                citynum] + img_date + '.jpg')
                        except:
                            continue


#某个地区的一组图片
def city_img():
    citynum=0
    for url in city_href:
        header = {
            'User-Agent':UserAgent,
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language': 'zh-CN',
            #'Referer': 'https://tianqi.moji.com/liveview/china/hubei/yunyang-district',
            'Host': 'tianqi.moji.com',
            'X-Requested-With': 'XMLHttpRequest' }
        req = urllib.request.Request(url, None, header)
        try:
            response = urllib.request.urlopen(req)
        except:
            continue
        the_page = response.read().decode('utf-8')
        soup = BeautifulSoup(the_page, "html.parser")
        all_imgid = soup.find_all('li', class_="scenery_item clearfix")
        ID = {}
        x = 0
        #得到各图片的id
        for img in all_imgid:
            id = img.get('data-id')
            ID[x] = id
            x += 1
        get_imgMessage(ID,citynum)
        citynum+=1

if __name__=='__main__':
    i=0
    for city_url in citys_url:
        ee=ee[i]
        city_href,city_name=getCitys(city_url)
        city_img()
        i+=1
