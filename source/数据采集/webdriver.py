#-*- coding:utf-8 -*-
from urllib.request import urlretrieve
import urllib.parse
import urllib3
import requests
import http.cookiejar
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import time
import re

Url='https://www.aqistudy.cn/historydata/daydata.php?city=%E5%8C%97%E4%BA%AC&month=2013-12'
UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
txtPath="D:\\100D5300\\PM_Data.txt"
conn = pymysql.connect(host='localhost',user='root',passwd='w904403',db='pm25data',port=3306,charset='utf8')
cursor = conn.cursor()

def getwebs():
    url="https://www.aqistudy.cn/historydata/"
    headers = {'User-Agent': UserAgent}
    #citys={1:'上海',2:'天津',3:'重庆'}
    citys={1:'西安',2:'太原'}
    #将中文进行编码
    cityEncode = urllib.parse.urlencode(citys)
    #分出地点的对应编码
    result= re.split('=|&',cityEncode)
    city_code={}
    tag=0
    for i in range(int(len(result)/2)):
        city_code[tag] = result[2*i+1]
        tag += 1
    citycode=1
    for city in city_code:
        print("正爬取"+citys[citycode]+'市的数据……')
        #f.write(citys[1]+'\n')
        month_href={}
        month_url = url+"monthdata.php?city=" + city_code[city]
        city_req = urllib.request.Request(month_url, None, headers)
        city_response = urllib.request.urlopen(city_req)
        data = city_response.read().decode('utf-8')
        tree = etree.HTML(data)
        for one in tree.xpath('//ul[@class="unstyled1"]'):
            month_href = one.xpath('.//li//a/@href')
        for each_month in range(len(month_href)):
            month = month_href[each_month].split('&')[1]
            print(month)
            day_url = url+"daydata.php?city=" + city_code[city]+"&"+month
            #print(day_url)
            #获取每日PM2.5数据
            getPM_data(citys[citycode],day_url)
        citycode+=1

def getPM_data(cityname,url):
    #cityname='保定'
    #months=['2015-04','2015-11','2016-06']
    print("selenium爬取数据中……")
    #for kk in months:
    #aurl = 'https://www.aqistudy.cn/historydata/daydata.php?city=%E4%BF%9D%E5%AE%9A&month='+kk
    header = {'User-Agent': UserAgent}
    # 利用selenium爬取数据
    driver = webdriver.Chrome()
    #driver.implicitly_wait(30)
    driver.get(url)
    time.sleep(5)
    k = 2
    for i in driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr')[1:]:
        td_id = 0
        currentTime = ''
        pm25 = 0
        for j in driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr[' + str(k) + ']/td'):
            if td_id == 0:
                # f.write('时间:'+j.text+' ')
                print("时间：" + j.text)
                currentTime = j.text
            if td_id == 3:
                # f.write('pm2.5:'+j.text+'\n')
                print("pm2.5：" + j.text)
                pm25 = int(j.text)
            td_id += 1
        try:
            cursor.execute("insert into pm_data(each_time,city,PM25) values(%s,%s,%s)",(currentTime, cityname, pm25))
        except:
            continue
        conn.commit()
        k += 1
    time.sleep(1)
    # 关闭当前浏览器
    driver.quit()

if __name__=='__main__':
    #f=open(txtPath,"w")
        getwebs()
   # for i in range(1,7):
      # getPM_data()
    #f.close()
