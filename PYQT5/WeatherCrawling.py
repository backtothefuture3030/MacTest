import requests
from bs4 import BeautifulSoup as bs 

class GoogleWeather():
    url ='https://www.google.com/search?q=%EB%82%A0%EC%94%A8&sxsrf=AOaemvIqL3SI7FEYqzuS-zStZFIRZxHjgQ%3A1636440017561&ei=0ReKYYO1IYDc2roPh9i8sA0&oq=%EB%82%A0%EC%94%A8&gs_lcp=Cgdnd3Mtd2l6EAMyDwgjELADECcQnQIQRhCAAjITCAAQgAQQhwIQsQMQgwEQsAMQFDIOCAAQgAQQsQMQgwEQsAMyDggAEIAEELEDEIMBELADMgsIABCABBCxAxCwAzIICAAQgAQQsAMyCAgAEIAEELADMgkIABCwAxAHEB4yCQgAELADEAcQHjIJCAAQsAMQBxAeSgQIQRgBUABYAGD0BGgBcAB4AIABAIgBAJIBAJgBAMgBCsABAQ&sclient=gws-wiz&ved=0ahUKEwjD4cSP1or0AhUArlYBHQcsD9YQ4dUDCA4&uact=5'
    headers = {
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    result = []

    def __init__(self, keyword = None):
        self.keyword = keyword

    def set_keyword(self, keyword):
        self.keyword = keyword
    
    def run(self):
        res = requests.get(self.url.format(self.keyword), headers = self.headers)
        self.parse_html(res.text)
        return res

    def parse_html(self, text):
        html = bs(text, 'html.parser')
        loc = html.find('div', {'id': 'wob_loc'})
        loc = loc.string if loc else loc
        time = html.find('div', {'id':'wob_dts'})
        time = time.string if time else time
        status = html.find('span', {'id':'wob_dc'})
        status = status.string if status else status
        self.result.append({
            'loc':loc,
            'time':time,
            'status':status
        })
    
    def get_result(self):
        if self.result:
            return self.result[-1]
        else:
            return None

if __name__== '__main__':
    crawler = GoogleWeather()
    while True:
        k = input("지역명 : ")
        crawler.set_keyword(k + " 날씨")
        crawler.run()
        r = crawler.get_result()
        for v in r.values(): print(v)
        print('-'*50)