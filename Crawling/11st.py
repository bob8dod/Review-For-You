# 11번가는 API를 통해 리뷰를 받아옵니다. 11번가는 쿠팡과 다르게 1page에 정해진 size가 있음
import json
from urllib.request import urlopen

products = 2661368800
num = 0

for pageNo in range(1, 50):
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
