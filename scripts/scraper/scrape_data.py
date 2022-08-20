from concurrent.futures import ThreadPoolExecutor
import re
from time import sleep
import requests
from bs4 import BeautifulSoup, Tag
from tqdm import tqdm
from glob import glob
from json import dumps
URLS = []

RETRIEVED_URLS = set()

with open('/home/miguel/Workspace/scraper/downloaded_urls.txt', 'r') as f:
    RETRIEVED_URLS = set(f.read().split('\n'))

with open('/home/miguel/Workspace/scraper/urls.txt', 'r') as f:
    URLS = f.read().split('\n')


URLS = [x for x in URLS if x not in RETRIEVED_URLS]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

fields = set()
location_fields = set()


def get_price(html):
    first_div = html.find('div', {'data-testid': 'ad-price-wrapper'})

    if not first_div:
        return None

    value = first_div.find('h2').text
    value = value.replace('R$ ', '').replace('.', '').replace(',', '')

    if value:
        return int(value)

    else:
        return None


def get_properties(html):
    first_div = html.find('div', {"data-testid": "ad-properties"})

    properties = {}

    if not first_div:
        return properties

    divs = first_div.find_all('div')

    for div in divs:
        field = div.find('dt').get_text()
        value = div.find('dd')

        if not value:
            value = div.find('a')

        value = value.get_text()

        properties[field] = value
        fields.add(field)

    return properties


def get_location(html):
    first_div = html.find('div', {"class": "realEstateLocation"})

    properties = {}

    if not first_div:
        return properties

    divs = first_div.find_all(
        'div', {'class': 'sc-hmzhuo sc-1f2ug0x-3 ONRJp sc-jTzLTM iwtnNi'})

    for div in divs:
        field = div.find('dt').get_text()
        value = div.find('dd')

        if not value:
            value = div.find('a')

        value = value.get_text()

        value = str(value.replace("m²", "").replace("R$ ", ""))

        if value.isnumeric():
            value = int(value)

        properties[field] = value
        fields.add(field)

    return properties


def retrieve_fields_from_page(content, retries=0):
    try:
        # page = requests.get(url, headers=headers)

        soup = BeautifulSoup(content, "html.parser")

        data = {
            "price": get_price(soup),
            "location": get_location(soup),
            "properties": get_properties(soup),
        }

        return data
    except:
        return None


def do_request(url, index, retries=0):
    try:
        page = requests.get(url, headers=headers)


        with open('/home/miguel/Workspace/scraper/downloaded_urls.txt', 'a') as f:
          f.write(url)

        with open(f'/home/miguel/Workspace/scraper/data/{index}.html', 'w+') as f:
          f.write(page.text)

    except KeyboardInterrupt:
      exit()
    except:
        print(url)
        print("waiting 10 seconds")
        if retries <= 2:
            sleep(10)
            do_request(url, index, retries+1)
        else:
          return None
    
FILES = glob('/home/miguel/Workspace/scraper/data/*.html')

data = []

for file in tqdm(FILES):
  content = None
  with open(file, 'r') as f:
    content = f.read()

  properties = retrieve_fields_from_page(content)

  if properties:
    data.append(properties)



# pages = []
# count = 0

# for i, url in enumerate(tqdm(URLS)):

#     do_request(url, i+651)

    # pages.append(page)

    # if i > 0 and i % 200 == 0:
    #    sleep(10)

    #         if not item:
    #           continue

    #         soup = BeautifulSoup(page.content, "html.parser")

    #         data.append(retrieve_fields_from_page(url, soup))

    #     pages = []


with open('/home/miguel/Workspace/scraper/data.json', 'w+') as f:
    f.write(dumps(data))
