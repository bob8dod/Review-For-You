# 쿠팡은 html 태그 경로를 통해서 받아옵니다.
import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
product_ID = 4500440492
size = 10
num = 0

for page in range(1,101):
    try:
        url = 'https://www.coupang.com/vp/product/reviews?productId={}&page={}&size={}&sortBy=ORDER_SCORE_ASC&ratings&q&viRoleCode=3&ratingSummary=true'.format(
            product_ID, page, size)
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        for s in range(size):
            review = re.sub('[\n\s]+',' ', soup.select('article')[s].text)
            num += 1
            print(num, review)
    except:
        print('리뷰가 끝입니다. 총',num,'개')
        break
