# 쿠팡은 html 태그 경로를 통해서 받아옵니다.
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
product_ID = 230142363
size = 10
num = 0

url_basic = 'https://www.coupang.com/vp/products/{}'.format(product_ID)
url_cate = url_basic + '/breadcrumb-gnbmenu'

data = requests.get(url_basic, headers=headers)
data_cate = requests.get(url_cate, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
soup_cate = BeautifulSoup(data_cate.text, 'html.parser')

category_path = soup_cate.find_all('a', attrs={'class': 'breadcrumb-link'})
categories = []
for cate in category_path:
    category = re.sub('[\n\s]+','',cate.text)
    categories.append(category)

product_name = soup.find('meta',attrs={'property':'og:title'})['content']
img_src = soup.find('meta',attrs={'property':'og:image'})['content']
price = soup.find('span', attrs={'class': 'total-price'}).text.strip()
print(categories, price)
print(product_name)
print(img_src)

print('===================================================')
for page in range(1, 2):
    try:
        url = 'https://www.coupang.com/vp/product/reviews?productId={}&page={}&size={}&sortBy=ORDER_SCORE_ASC&ratings&q&viRoleCode=3&ratingSummary=true'.format(
            product_ID, page, size)
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        for s in range(size):
            review = re.sub('[\n\s]+', ' ', soup.select('article')[s].text)
            num += 1
            print(num,'|',review,sep='')
    except:
        print('리뷰가 끝입니다. 총', num, '개')
        break
