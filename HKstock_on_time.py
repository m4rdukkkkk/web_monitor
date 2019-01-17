

# ! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from lxml import etree
import time
import datetime
#  2019.1.13  中国燃气-恒生指数

total_Cash = 100000
index_Cash = 0.3*total_Cash
stock_Cash = 0.6*total_Cash
# FX_price = 6.95  都按照日元测算
index_Future_N = (index_Cash)/20222 #向下取整 
index_cost = 26666
stock_cost = 26.1

def get_index_PL():
    response = requests.get('https://www.laohu8.com/hq/s/HSI?f=baidu&utm_source=baidu&utm_medium=aladingpc')
    html = response.text
    selector = etree.HTML(html)
    price = selector.xpath('//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/strong/text()')
    items_float = float(price[0])
    indexF_PL = (index_cost-items_float)*10  # mini恒指的交易乘数是10
    indexF_PL_2 = round(indexF_PL,2)
    big_list.append(str(indexF_PL_2))


# 00384 中国燃气 25.4
def get_stocks_PL():
    response = requests.get('https://www.laohu8.com/hq/s/00384')
    html = response.text
    selector = etree.HTML(html)
    price = selector.xpath('//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/strong/text()')
    stock_PL = (float(price[0]) - stock_cost)/stock_cost * (stock_Cash)  # 直接用价格做百分比计算即可
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
        total_profit_R_2 = '%.2f%%' % (total_profit_R * 100)
        big_list.append(total_profit_R_2)

    except IndexError as e:
        print(e)







def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='web_monitor',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    if len(big_list) == 4:
        cursor.executemany('insert into MHI_OneStock_PL (index_PL,stock_PL,profilo_PL,profilo_PL_R) values (%s,%s,%s,%s)', content)
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
#
# create table MHI_OneStock_PL(
# id int not null primary key auto_increment,
# index_PL varchar(10),
# stock_PL varchar(10),
# profilo_PL varchar(10),
# profilo_PL_R varchar(10)
# ) engine=InnoDB  charset=utf8;
