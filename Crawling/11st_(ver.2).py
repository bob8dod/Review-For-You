# 11번가는 API를 통해 리뷰를 받아옵니다. 11번가는 쿠팡과 다르게 1page에 정해진 size가 있음
import json
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
products = 2266546423

url_basic = 'https://www.11st.co.kr/products/{}'.format(products)
data = requests.get(url_basic, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

try:
    category_path = soup.find('div', attrs={'class':'c_product_category_path'}).find_all('em', attrs={'class':'selected'})
    categories = []
    for cate in category_path:
        categories.append(cate.text)
    product_name = soup.find('h1', attrs={'class':'title'}).text.strip()
    img_src = soup.find('div', attrs={'class':'img_full'}).find('img')['src']
    price = soup.find('ul', attrs={'class':'price_wrap'}).find('span',attrs={'class':'value'}).text
    print(categories, price)
    print(product_name)
    print(img_src)
except: # For Amazon
    name = soup.find('meta',attrs={'property':'og:title'})['content']
    cate_price = soup.find('meta',attrs={'property':'og:description'})['content'].strip()
    img = soup.find('meta',attrs={'property':'og:image'})['content']
    print(name)
    print(cate_price)
    print(img)

print('===================================================')

num = 0
for pageNo in range(1, 2):
    try:
        url = 'https://m.11st.co.kr/products/v1/app/products/{}/reviews/list?pageNo={}&sortType=01&pntVals=&rtype=&themeNm='.format(products, pageNo)
        response = urlopen(url)
        json_data = json.load(response)
        for i in range(len(json_data['review']['list'])):
            if json_data['review']['list'][i]['subject']:
                num += 1
                print(num,'|', json_data['review']['list'][i]['subject'],sep='')

    except:
        print('리뷰가 끝났습니다. 총 개수:', num)
