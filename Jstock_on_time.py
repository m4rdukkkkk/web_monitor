# -*- coding:utf8 -*-



import re
import datetime
import time
import requests
from pymongo import MongoClient
import pymysql




#使用一个字符串分割然后再拼接，去除掉分隔符号！


def get_index():
    response = requests.get('https://stocks.finance.yahoo.co.jp/stocks/detail/?code=998407.O')
    html = response.text
    patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    item = re.findall(patt,html)
    for i in item:
        a = i.split(',')[0]
        b = i.split(',')[1]
        c = a + b
        big_list.append(c)



def get_stocks():
    response = requests.get('https://stocks.finance.yahoo.co.jp/stocks/detail/?code=8961.T')
    html = response.text
    patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    item = re.findall(patt,html)
    for i in item:
        a = i.split(',')[0]
        b = i.split(',')[1]
        c = a + b
        big_list.append(c)

#浮点数

def get_spread():
    A = big_list[0]
    B = big_list[1]
    C = float(A)/float(B)
    W = "%.6f" % C
    big_list.append(W)



#尝试添加到三个不同的数据库看看哪个更好用！
# 先把爬取和存储的问题全部解决，后面再解决实时可视化的问题！
#highcharts，可视化就属于前端的部分了,慢慢来吧，监控工具改装一下，就是跟盘的工具！
#redis还是不适合多个键，多个值同时出现的场景！



# def insert_to_Mongo(item):
#     client = MongoClient(host='localhost',port=27017)   #链接连接数据库
#     db = client.On_time_DT       #建立数据库
#     p = db.ontime_dt            #在上面数据库中建立集合（表）
#     result = p.insert(item)  # 添加内容
#     print(result)



    # spread = int(A)/int(B)
    # big_list.append(spread)

# 存入MySQL中
def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.executemany('insert into j_stocks (indexs,stock,spread) values (%s,%s,%s)', content)
    connection.commit()
    connection.close()
    print('向MySQL中添加数据成功！')

#有必要专门做一个监控系统！以来flask或Django，



if __name__ == '__main__':
    while True:
        big_list = []
        get_index()
        get_stocks()
        get_spread()
        # con_dict = {
        #     'time':datetime.datetime.now(),
        #     'index':big_list[0],
        #     'stock':big_list[1],
        #     'spread':big_list[2],
        # }
        # insert_to_Mongo(con_dict)

        time.sleep(3)

        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        # print(content)


