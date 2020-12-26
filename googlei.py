import pycurl
import json

import io as bytesIOModule
from bs4 import BeautifulSoup

import certifi

SEARCH_URL = 'https://www.google.com/searchbyimage?&image_url='


def search(url):
    code = doImageSearch(url)
    return parseResults(code)


def doImageSearch(image_url):
    """Perform the image search and return the HTML page response."""


    returned_code = bytesIOModule.BytesIO()
    full_url = SEARCH_URL + image_url


    conn = pycurl.Curl()

    conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    return returned_code.getvalue().decode('UTF-8')



def parseResults(code):
    """Parse/Scrape the HTML code for the info we want."""

    soup = BeautifulSoup(code, 'html.parser')

    results = {
        'links': [],
        'descriptions': [],
        'titles': [],
        'similar_images': [],
        'best_guess': ''
    }

    for div in soup.findAll('div', attrs={'class': 'rc'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])

    for desc in soup.findAll('span', attrs={'class': 'st'}):
        results['descriptions'].append(desc.get_text())

    for title in soup.findAll('h3', attrs={'class': 'r'}):
        results['titles'].append(title.get_text())

    for similar_image in soup.findAll('div', attrs={'rg_meta'}):
        tmp = json.loads(similar_image.get_text())
        img_url = tmp['ou']
        results['similar_images'].append(img_url)

    for best_guess in soup.findAll('a', attrs={'class': 'fKDtNb'}):
      results['best_guess'] = best_guess.get_text()

    return results

def main():
    print(search("https://assets.poketwo.net/images/151.png"))

if __name__ == '__main__':
    main()
