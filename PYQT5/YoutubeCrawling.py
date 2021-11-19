# selenium , bs4 혼합 사용시 빠르고 간편하다.

from selenium.webdriver import Chrome
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib import parse
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QDial, QDialog, QMainWindow
import re


class Youtube():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    url = 'https://www.youtube.com/'
    driver = Chrome(options=options)
    driver.get(url)

    scroll_pane_height = driver.execute_script('return document.documentElement.scrollHeight')  # 스크롤 바 내리기

    while True:
        # 스크롤바를 스크롤패인 높이 만큼 이동
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight)')
        # 밑에 붙일 내용을 요청해서 시간차를 둔다
        time.sleep(1)
        new_scroll_pane_height = driver.execute_script('return document.documentElement.scrollHeight')
        #print(scroll_pane_height, new_scroll_pane_height)
        if scroll_pane_height == new_scroll_pane_height:
            break
        scroll_pane_height = new_scroll_pane_height


    soup = BeautifulSoup(driver.page_source)
    a_list = soup.select('div#contents div#content a#video-title-link')
    titles = []
    links = [] 
    for a_tag in a_list:
        link = parse.urljoin(url, a_tag.get('href'))  # url 의 상대경로를 절대경로로 바꾼다.
        title = a_tag.text
        titles.append(title)
        links.append(link)

    for i in range(0,len(titles)):
        print(titles[i] + "\n"+": " + links[i])




