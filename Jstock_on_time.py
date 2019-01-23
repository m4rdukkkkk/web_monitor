

# ! -*- coding:utf-8 -*-
# 增加index部位的手数
import time
import re
import pymysql
import requests
from lxml import etree
import time
import datetime
from math import floor
# 2019.1.23 修改日经套利模型的参数比例
# 日经期货225的化429点就翻倍了，6:3的比例就不合适了
# 尝试缩放到7：１
# 日经也是一条毒蛇啊


# 2019.1.13 大日本住友製薬(株)【4506 -——————日经225指数
total_Cash = 10000000 # 初识资金1000万日元　
index_Cash = 0.1*total_Cash
stock_Cash = 0.7*total_Cash
index_Future_N = floor(index_Cash/429000)# index的手数，向下取整。
index_cost = 20359.00
stock_cost = 3635

def get_index_PL():
    response = requests.get('https://stocks.finance.yahoo.co.jp/stocks/detail/?code=998407.O')
    html = response.text
    patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    items = re.findall(patt,html)
    items_str = "".join(items[0].split(','))
    items_float = float(items_str)
    indexF_PL = (index_cost-items_float)*1000*index_Future_N  # index部位的价差，乘以每点1000日元，再乘以手数，最终是日元盈亏
    indexF_PL_2 = round(indexF_PL,2)
    big_list.append(str(indexF_PL_2))


# 大日本住友製薬(株)【4506】
def get_stocks_PL():
    url = 'https://stocks.finance.yahoo.co.jp/stocks/detail/?code=4506'
    headers = {'Useragent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
    response = requests.get(url, headers=headers)
    content = response.text
    patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    items = re.findall(patt, content)
    price_str = "".join(items[0].split(','))
    stock_PL = ((int(price_str) - stock_cost)/stock_cost) * stock_Cash # 股价涨跌幅，乘以stock总资金
    stock_PL_2 = round(stock_PL,2)
    big_list.append(stock_PL_2)




def profilo_PL():
    try:
        A = big_list[0]
        B = big_list[1]
        profilo_PL =  float(B) + float(A)
        profilo_PL_2 = round(profilo_PL,2)
        big_list.append(profilo_PL_2)
        total_profit_R = profilo_PL_2/total_Cash
        # total_profit_R_2 = '%.2f%%' % (total_profit_R * 100)  这个是为加上　％
        total_profit_R_2 = round(total_profit_R,3) * 100  # 这个最简单

        big_list.append(total_profit_R_2)

    except IndexError as e:
        print(e)








def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    if len(big_list) == 4:
        cursor.executemany('insert into J225_OneStock_PL (index_PL,stock_PL,profilo_PL,profilo_PL_R) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    else:
        print('出列啦')
#
#
if __name__ == '__main__':
    while True:
        big_list = []
        get_index_PL()
        get_stocks_PL()
        profilo_PL()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        time.sleep(10)
        print(datetime.datetime.now())

#  指数期货盈亏， 个股盈亏，总盈亏， 总收益率   这个四个部分进行设计


#
# #
# create table J225_OneStock_PL(
# id int not null primary key auto_increment,
# index_PL varchar(10),
# stock_PL varchar(10),
# profilo_PL varchar(10),
# profilo_PL_R varchar(10)
# ) engine=InnoDB  charset=utf8;


# drop table J225_OneStock_PL;
