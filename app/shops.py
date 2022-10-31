from bs4 import BeautifulSoup as bs
import requests as r
import random

base_url = 'https://www.amazon.sg'

# Product Name > Price > Url > Image
def randomCategories(s):
    span = s.find('span', text='Any Category')
    return {i.text:i['href'] for i in span.parent.parent.find_all('a')}

def returnCategory(d):
    last = len(d)
    key = list(d.keys())[random.randint(0,last-1)]
    return key, d[key]

def getProductInfo(li):
    links = li.find_all('a')
    # productInfo = li.find('span', {'class':'aok-inline-block zg-item'})
    productName = ''.join(list(map(str.strip, links[1].span.text.split('\n'))))
    try:
        productLowestPrice = links[3].text.strip('\n')
    except:
        productLowestPrice = '-'
    productURL = base_url + links[1]['href']
    productImage = links[0].img['src']
    names = ["name", "price", "url", "img"]
    return {i:j for i,j in zip(names,(productName,productLowestPrice,productURL,productImage))}

def returnProducts(url, n):
    s = bs(r.get(url).content, 'html.parser')
    category, url_1 = returnCategory(randomCategories(s))
    page_source = bs(r.get(base_url + url_1).content,'html.parser')
    products = page_source.find_all('div', {'id': 'gridItemRoot'})
    d = {'category': category}
    d.update({'items':[getProductInfo(i) for i in products[:n]]})
    return d