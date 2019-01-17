

# ! -*- coding:utf-8 -*-

import time
import re
import pymysql
import requests
from selenium import webdriver
# 还是要用PhantomJS
import datetime
import string

total_Cash = 30000
index_Cash = 0.3*total_Cash
stock_Cash = 0.6*total_Cash
FX_price = 6.95
index_Future_N = (index_Cash/FX_price)/1000 #向下取整
index_cost = 10500
stock_cost = 2.40

# 2019.1.7 远兴能源——————a50指数模型测试(重新关注，有了接口)



def get_index_PL():
    try :

        driver = webdriver.Chrome()
        url = 'https://finance.sina.com.cn/futures/quotes/CHA50CFD.shtml'
        # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        driver.set_window_size(38, 12)  # 设置窗口大小
        driver.get(url)
        # time.sleep(1)
        html = driver.page_source
        # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧
        patt = re.compile('<th>最新价:' + '.*?</th><td class=".*?">(.*?)</td>', re.S)
        items = re.findall(patt, html)
        items_int = int(items[0][:-3])
        indexF_PL = (index_cost-items_int)*FX_price
        indexF_PL_2 = round(indexF_PL,2)
        big_list.append(str(indexF_PL_2))
        driver.quit()
    except ValueError as e:
        pass



# 远兴能源
def get_stocks_PL():
    url = 'https://www.laohu8.com/hq/s/000683'
    headers = {'Useragent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
    response = requests.get(url, headers=headers)
    content = response.text
    patt = re.compile('<td class="price">(.*?)</td>', re.S)
    items = re.findall(patt, content)
    stock_PL = (float(items[0])-stock_cost) *(stock_Cash/stock_cost)
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
        cursor.executemany('insert into A50_OneStock_PL (index_PL,stock_PL,profilo_PL,profilo_PL_R) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    else:
        print('出列啦')

#
# #
# 尝试数据源不一定稳定，勉强可以用下
if __name__ == '__main__':
    i = 0  
    while True:
        
        i += 1
        print(i)
        big_list = []
        get_index_PL()
        get_stocks_PL()
        profilo_PL()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        time.sleep(6)







# create table A50_OneStock_PL(
# id int not null primary key auto_increment,
# index_PL varchar(10),
# stock_PL varchar(10),
# profilo_PL varchar(10),
# profilo_PL_R varchar(10)
# ) engine=InnoDB  charset=utf8;

# drop table A50_OneStock_PL;
