import time
import requests
import csv
from bs4 import BeautifulSoup as soup
import requests


electronic_url = [
    'https://paytmmall.com/nce-smartphones-llpid-281608?discoverability=online&use_mw=1&src=store&from=storefront&page=',
    'https://paytmmall.com/laptops-glpid-6453?use_mw=1&src=store&from=storefront&page='
]

headers = {'accept': '*/*',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
                   'cache-control': 'no-cache',
                   'dnt': '1',
                   'pragma': 'no-cache',
                   'referer': 'https',
                   'sec-fetch-mode': 'no-cors',
                   'sec-fetch-site': 'cross-site',
                   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                   }


def get_requests(writer_, url_):
    a_response_ = requests.get(url=url_,
                               headers=headers)
    time.sleep(3)
    products_ = soup(a_response_.text, "html.parser")
    products = products_.find('div', {'class': '_3RA-'})
    for product in products.findAll('div', {'class': '_1fje'}):
        for product_ in product.findAll('div', {'class': '_2i1r'}):
            name = product_.find('div', {'class': 'UGUy'}).text
            price = product_.find('div', {'class': '_1kMS'}).text.replace(",", "")
            link = product_.find('a')['href']
            try:
                price_old = product_.find('div', {'class': 'dQm2'}).text
                price_old = price_old.split('-', 1)[0].replace(",", "")
            except:
                price_old = 0

            new_price = round(int(price)/73)
            old_price = round(int(price_old)/73)
            discount = old_price - new_price
            writer_.writerow([name, str(old_price), str(new_price), str(discount), "none", link])
            # print(product)


def start_scrapper():
    with open('PaytmLaptops.csv', 'w', newline='') as laptops:
        writer_laptop = csv.writer(laptops)
        # Laptops
        for i in range(1, 4):
            print(electronic_url[1] + str(i))
            get_requests(writer_laptop, electronic_url[0] + str(i))
            time.sleep(3)

    with open('PaytmMobiles.csv', 'w', newline='') as mobiles:
        writer_mobiles = csv.writer(mobiles)
        # Mobiles
        for i in range(1, 4):
            print(electronic_url[0] + str(i))
            get_requests(writer_mobiles, electronic_url[1] + str(i))
            time.sleep(3)


def test_m():
    print("ahaa12")