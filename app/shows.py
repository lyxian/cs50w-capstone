from bs4 import BeautifulSoup as bs
import requests as r
import random

# Show Name > Show Url > Show Image
def randomTag(s):
    n = len(s.find_all('h2'))-2
    return [i.text for i in s.find_all('h2')][random.randint(0,n)]

def getTag(tag, tagname):
    return tag.h2.text == tagname if tag.h2 else False

def showNames(div):
    return [i.find('span', {'class':'nm-collections-title-name'}).text for i in div.find_all('li')]

def showImages(div):
    try:
        return [i.find('img')['src'] for i in div.find_all('li') if 'https' in i.find('img')['src']]
    except:
        return []

def showURLs(div):
    return [i.find('a')['href'] for i in div.find_all('li')]

def returnPopularShows(url):
    s = bs(r.get(url).content, 'html.parser')
    genre = randomTag(s)
    print(genre)
    div = [tag for tag in s.find_all('section') if getTag(tag, genre)][0]
    names = showNames(div)
    images = showImages(div)
    urls = showURLs(div)
    n = len(images)
    if n == 0:
        return {'error': True}
    else:
        info = list(zip(names[:n],urls[:n],images))
        names = ["name", "url", "img"]
        genre = genre.split('Explore more')[0] if 'Explore more' in genre else genre
        return {'genre': genre, 'shows': [dict(zip(names,i)) for i in info]}