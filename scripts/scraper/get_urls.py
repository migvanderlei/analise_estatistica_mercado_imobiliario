import re
import requests
from bs4 import BeautifulSoup, Tag

LIST_URL = "https://am.olx.com.br/regiao-de-manaus/manaus/imoveis/venda?o={}"

UL_LIST_ID = "ad-list"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}



def retrieve_ads_from_page(url):
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    ads_list_ul = soup.find("ul", {"id": UL_LIST_ID})

    ads_list = []

    for item in ads_list_ul.findAll('li'):
      if isinstance(item, Tag):
        div = item.find('div')
        a = div.find('a')
        if a:
          ads_list.append(a.get('href'))
    print(f"retrieved {len(ads_list)} ads")
    return ads_list


def retrieve_ads_list(count=100):
    ads_url_list = []

    url = ''

    for i in range(count):
        url = LIST_URL.format(i+1)

        print('getting page', i+1)
        ads_url_list += retrieve_ads_from_page(url)
    
    return ads_url_list

ads_url_list = retrieve_ads_list()
with open('/home/miguel/Workspace/scraper/urls.txt', 'w+') as f:
  f.write("\n".join(ads_url_list))