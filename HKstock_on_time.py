
#! -*- coding:utf-8 -*-

import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import requests
from multiprocessing import Pool
# driver = webdriver.Chrome()
# 还必须要用selenium解决js渲染的问题 ,还是要寻找不用渲染的，因为要计算价差，同时解决两个渲染外加计算负担太大
#恒生指数  老虎证券

def get_index():
    url = 'https://www.laohu8.com/hq/s/HSI'
    response = requests.get(url)
    content =  response.text
    patt = re.compile('<td class="price">(.*?)</td>',re.S)
    items = re.findall(patt,content)
    for ite in items:
        big_list.append(ite)


def get_stocks():
    url = 'https://www.laohu8.com/hq/s/00700'
    response = requests.get(url)
    content =  response.text
    patt = re.compile('<td class="price">(.*?)</td>',re.S)
    items = re.findall(patt,content)
    for ite in items:
        big_list.append(ite)



def get_spread():
    A = big_list[0]
    B = big_list[1]
    C = float(A)/float(B)
    W = "%.6f" % C
    big_list.append(W)




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.executemany('insert into hk_stocks (indexs,stock,spread) values (%s,%s,%s)', content)
    connection.commit()
    connection.close()
    print('向MySQL中添加数据成功！')



if __name__ == '__main__':
    while True:
        big_list = []
        get_index()
        get_stocks()
        get_spread()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        time.sleep(2)
        insertDB(content)
