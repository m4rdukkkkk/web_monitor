
#! -*- coding:utf-8 -*-


import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.request
import time
from multiprocessing import Pool
driver = webdriver.Firefox()
# 还必须要用selenium解决js渲染的问题
#恒生指数

def get_index():
    url = 'https://www.hsi.com.hk/schi'

    driver.get(url)
    html = driver.page_source
    print(html)
    # patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    # item = re.findall(patt,html)
    # for i in item:
    #     a = i.split(',')[0]
    #     b = i.split(',')[1]
    #     c = a + b
    #     big_list.append(c)

get_index()