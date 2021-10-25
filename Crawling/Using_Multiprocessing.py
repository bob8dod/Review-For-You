def Crawling(product_num, pageNo):
    try:
        url = 'https://m.11st.co.kr/products/v1/app/products/{}/reviews/list?pageNo={}&sortType=01&pntVals=&rtype=&themeNm='.format(
            product_num, pageNo)
        response = urlopen(url)
        json_data = json.load(response)['review']['list']
        temp = []
        for rev in json_data:
            if rev['subject']:
                review = rev['subject']
                score = str(rev['evlPnt'])
                xai_before_text, xai_value, xai_positive_negative = DNN_func(review)
                temp.append([score, review,xai_before_text,xai_value,xai_positive_negative])
        return temp
    except:
        pass

def lets_do_crawling(product_num):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url_basic = 'https://www.11st.co.kr/products/{}'.format(product_num)
    data = requests.get(url_basic, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    category_path = soup.find('div', attrs={'class': 'c_product_category_path'}).find_all('em', attrs={
        'class': 'selected'})
    categories = ''
    for cate in category_path:
        if categories == '':
            categories = cate.text
        else:
            categories = categories + ', ' + cate.text

    product_name = re.sub('[/]', ' ', soup.find('h1', attrs={'class': 'title'}).text).strip()
    img_src = soup.find('div', attrs={'class': 'img_full'}).find('img')['src']
    price = soup.find('ul', attrs={'class': 'price_wrap'}).find('span', attrs={'class': 'value'}).text

    review_len = soup.find('strong', attrs={'class': 'text_num'}).text
    review_len = int(re.sub('[^0-9]', '', review_len))

    pool = Pool(4)
    func = partial(Crawling,product_num)
    tem = pool.map(func, range(1,51))
    pool.close()
    pool.join()

    text = [j for i in tem for j in i]
    tem_data = pd.DataFrame(text, columns=['score', 'review','xai_before_text','xai_value','xai_positive_negative'])
    tem_data.drop_duplicates(['review'], inplace=True)
    tem_data.reset_index(drop=True, inplace=True)
    result, keyword, vocab_sorted, review_data = result_of_code([*map(lambda x : [x[0],x[1]], text)])

    return tem_data, product_name, img_src, price, review_len, categories, result, keyword
