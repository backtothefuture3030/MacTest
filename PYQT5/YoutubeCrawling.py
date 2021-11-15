import selenium
from selenium import webdriver
from time import sleep
import time

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
    titles.append(title.get_attribute('href'))


driver.quit()