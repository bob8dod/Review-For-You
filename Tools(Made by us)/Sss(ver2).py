import json
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool, Manager

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
products = 3356951618
# https://www.11st.co.kr/products/3356951618?trTypeCd=PW24&trCtgrNo=585021
url_basic = 'https://www.11st.co.kr/products/{}'.format(products)
data = requests.get(url_basic, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

category_path = soup.find('div', attrs={'class': 'c_product_category_path'}).find_all('em', attrs={'class': 'selected'})
categories = set()
for cate in category_path:
    categories.add(cate.text)
product_name = soup.find('h1', attrs={'class': 'title'}).text.strip()
img_src = soup.find('div', attrs={'class': 'img_full'}).find('img')['src']
price = soup.find('ul', attrs={'class': 'price_wrap'}).find('span', attrs={'class': 'value'}).text
print(product_name)
print(categories, price)
print(img_src)
# except: # For Amazon
#     name = soup.find('meta',attrs={'property':'og:title'})['content']
#     cate_price = soup.find('meta',attrs={'property':'og:description'})['content'].strip()
#     img = soup.find('meta',attrs={'property':'og:image'})['content']
#     print(name)
#     print(cate_price)
#     print(img)

manager = Manager()
text = manager.list()
score = manager.list()


def Crawling(pageNo):
    num = 0

    try:
        url = 'https://m.11st.co.kr/products/v1/app/products/{}/reviews/list?pageNo={}&sortType=01&pntVals=&rtype=&themeNm='.format(
            products, pageNo)
        response = urlopen(url)
        json_data = json.load(response)
        for i in range(len(json_data['review']['list'])):
            if json_data['review']['list'][i]['subject']:
                num += 1
                text.append(''.join([str(num), '|', json_data['review']['list'][i]['subject']]))
                score.append(json_data['review']['list'][i]['evlPnt'])
    except:
        pass


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=8)  # 4개의 프로세스 동시에 작동
    pool.map(Crawling, range(1, 1000, 10))  # title_to_list라는 함수에 1 ~ end까지 10씩늘려가며 인자로 적용
    pool.close()
    pool.join()
    print(len(text))
    print("실행 시간 : %s초" % (time.time() - start_time))
