# -*- coding:utf8 -*-


import re
import datetime
import time
import requests
from pymongo import MongoClient
import pymysql




#中证500


def get_index():
    response = requests.get('http://finance.sina.com.cn/futures/quotes/IC0.shtml')
    html = response.text
    # patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    # item = re.findall(patt,html)
    # for i in item:
    #     a = i.split(',')[0]
    #     b = i.split(',')[1]
    #     c = a + b
    #     big_list.append(c)