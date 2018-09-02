
#! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
# driver = webdriver.Chrome()
# 还必须要用selenium解决js渲染的问题 ,还是要寻找不用渲染的，因为要计算价差，同时解决两个渲染外加计算负担太大
#新浪爬实时数据不是很理想 应该是被反爬虫处理了，还是用的股市通

def get_index():
    headers = {'Useragent':'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'}
    url = 'https://gupiao.baidu.com/stock/sz399905.html'
    response = requests.get(url,headers=headers)
    content =  response.text
    patt = re.compile('<strong  class="_close">(.*?)</strong>',re.S)
    items = re.findall(patt,content)
    for ite in items:
        big_list.append(ite)




def get_stocks():
    url = 'https://gupiao.baidu.com/stock/sh600997.html'
    headers= {'Useragent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
    response = requests.get(url, headers=headers)
    content =  response.text
    patt = re.compile('<strong  class="_close">(.*?)</strong>',re.S)
    items = re.findall(patt,content)
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
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    #这里是判断big_list的长度，不是content字符的长度
    if  len(big_list) == 3:
        cursor.executemany('insert into a_stocks (indexs,stock,spread) values (%s,%s,%s)', content)
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
        time.sleep(1)
        get_stocks()
        time.sleep(1)
        get_spread()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)


#IndexError: list index out of range  如果出现这个错误就是因为开始没有抓取成功！，所以两个方案
#1.要保持数据连续，就每隔1秒  2. 或者用异常捕捉，其实两个最好都用上,出啊如数据库，如果len长度不等于3就不插入