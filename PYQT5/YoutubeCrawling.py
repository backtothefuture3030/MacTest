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

form_class = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/Youtubeb.ui')[0]

class Mywindow(QDialog, form_class):  # 윈도우 만들어주기, 조작 정의
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 버튼 기능 정의
        self.crawlStart.clicked.connect(self.clicked_crawlStart)  # [버튼] 크롤링 시작
        #self.articleTable.clicked.connect(self.clicked_articleTable) articleTable 열을 눌렀을때 url 연결 구현 (개발중)
    '''
    def clicked_articleTable(self): # # [버튼] articleTable의 링크 열을 눌렀을 때, 해당 링크로 연결
        if item.column() == 1:
            webbrowser.open('www.google.com')'''
    
    def Crawling():


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
    print(titles[i] + "  :  " + links[i])






