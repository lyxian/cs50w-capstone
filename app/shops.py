from bs4 import BeautifulSoup as bs
import requests as r
import random

# Product Name > Price > Url > Image
def randomCategories(s):
    return {i.text:i.a['href'] for i in s.find(id='zg_browseRoot').ul.find_all('li')}

def returnCategory(d):
    last = len(d)
    key = list(d.keys())[random.randint(0,last-1)]
    return key, d[key]

def getProductInfo(li):
    base_url = 'https://www.amazon.sg'
    productInfo = li.find('span', {'class':'aok-inline-block zg-item'})
    productName = li.find('div',{'aria-hidden':True}).text.strip()
    try:
        productLowestPrice = li.find_all('span', {'class':'p13n-sc-price'})[0].text
    except:
        productLowestPrice = '-'
    productURL = base_url + li.a['href']
    productImage = li.img['src']
    names = ["name", "price", "url", "img"]
    return {i:j for i,j in zip(names,(productName,productLowestPrice,productURL,productImage))}

def returnProducts(url, n):
    s = bs(r.get(url).content, 'html.parser')
    category, url_1 = returnCategory(randomCategories(s))
    page_source = bs(r.get(url_1).content,'html.parser')
    products = page_source.find('ol').find_all('li')
    d = {'category': category}
    d.update({'items':[getProductInfo(i) for i in products[:n]]})
    return d