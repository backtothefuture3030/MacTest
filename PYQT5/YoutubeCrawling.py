'''
import selenium
from selenium import webdriver
from time import sleep
import time

class YoutubeCrawler():
    url = 'https://www.youtube.com/'
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    titles = []
    href = []

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    driver.get(url)
    for i in range(2,7):
        title = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[7]/ytd-rich-item-renderer[{}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a'.format(i))
        titles.append(title.get_attribute('title'))
        href.append(title.get_attribute('href'))
    print(titles)
    print(href)

    driver.quit()

YoutubeCrawler()
'''
# selenium 을 이용하니까 pyqt 작동이 너무느리고 안통한다 bs4 를 사용하는게..

from bs4 import BeautifulSoup
import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate
import re

form_class = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/Youtubeb.ui')[0]

class MyWindow(QDialog, form_class):

