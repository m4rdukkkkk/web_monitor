
#! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from selenium import webdriver
#还是要用PhantomJS
from config import *
import datetime
# 国债期货成本过高，套利效果不是很明显！尝试思考A50新加坡股指期货与内盘个股的结合！


# 还必须要用selenium解决js渲染的问题 ,还是要寻找不用渲染的，因为要计算价差，同时解决两个渲染外加计算负担太大
#新浪爬实时数据不是很理想 应该是被反爬虫处理了，还是用的股市通

def get_index():
    driver = webdriver.Chrome()
    url = 'https://finance.sina.com.cn/futures/quotes/CHA50CFD.shtml'
    # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    driver.set_window_size(380,1200) #设置窗口大小
    driver.get(url)
    # time.sleep(1)
    html = driver.page_source
    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧
    patt = re.compile('<th>最新价:'+'.*?</th><td class=".*?">(.*?)</td>',re.S)
    items = re.findall(patt,html)
    for ite in items:
        big_list.append(ite)







# 远兴能源
def get_stocks():
    url = 'https://www.laohu8.com/hq/s/000683'
    headers= {'Useragent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
    response = requests.get(url, headers=headers)
    content =  response.text
    patt = re.compile('<td class="price">(.*?)</td>',re.S)
    items = re.findall(patt,content)
    print(datetime.datetime.now())
    print(items)
    for ite in items:
        big_list.append(ite)


def get_spread():
    try:
        A = big_list[0]
        B = big_list[1]
        C = float(A)/float(B)
        W = "%.6f" % C
        big_list.append(W)
    except IndexError as e :
        print(e)




def insertDB(content):
    connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    #这里是判断big_list的长度，不是content字符的长度
    if  len(big_list) == 3:
        cursor.executemany('insert into A50_myStock (indexs,stock,spread) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    else:
        print('出列啦')





#
# 尝试数据源不一定稳定，勉强可以用下
if __name__ == '__main__':
    while True:
        big_list = []
        get_index()
        get_stocks()
        get_spread()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)


#IndexError: list index out of range  如果出现这个错误就是因为开始没有抓取成功！，所以两个方案
#1.要保持数据连续，就每隔1秒  2. 或者用异常捕捉，其实两个最好都用上,出啊如数据库，如果len长度不等于3就不插入


# 2018.9.6 数据源进行调整 国债期货使用新浪财经，个股恋情老虎整证券，更加稳定