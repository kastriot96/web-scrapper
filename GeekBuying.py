import time
import requests
#import urllib3
import csv
from bs4 import BeautifulSoup as soup
import requests

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
    products = products_.find('ul', {'class': 'gridView'})
    if products is None:
        pass
    else:
        for product in products.findAll('li', {'class': 'searchResultItem'}):
            name = product.find('div', {'class': 'name'})
            url = name.find('a')['href']
            name = name.find('a').text.rstrip().strip(" ")
            try:
                price = product.find('div', {'class': 'price'}).text.strip("\n").strip(" ").strip("\r\n").strip(" ")
                price = price.split('.', 1)[0]
                price = price.replace("$", "")
            except:
                price = '0'
            try:
                price_old = product.find('div', {'class': 'list-price'}).text.strip("\n").strip(" ").strip("\r\n").strip(" ")
                price_old = price_old.split('.', 1)[0]
                price_old = price_old.replace("$", "")
            except:
                price_old = '0'
            print('name: ' + name.rstrip().strip('\t') + " price: " + price + " price_old: " + price_old, " url: " + url[1:10])
            try:
                if price_old == '0':
                    discount = 0
                elif price == '0':
                    discount = 0
                else:
                    discount = round(int(price_old)) - round(int(price))
            except:
                discount = 0

            writer_.writerow([name.rstrip(), price_old, price, str(discount), "none", url])


def start_scrapper():
    with open('GeekLaptops.csv', 'w', newline='') as laptops:
        writer_laptop = csv.writer(laptops)
        # Laptops
        for i in range(1, 4):
            get_requests(writer_laptop, 'https://www.geekbuying.com/category/Laptops-1974/'+str(i)+'-40-3-0-0-0-grid-0-ALL-0.html')
            time.sleep(3)
    #
    with open('GeekMobiles.csv', 'w', newline='') as mobiles:
        writer_mobiles = csv.writer(mobiles)
        # Laptops
        for i in range(1, 4):
            get_requests(writer_mobiles, 'https://www.geekbuying.com/category/Cell-Phones-1556/'+str(i)+'-40-3-0-0-0-grid-0-all-0.html')
            time.sleep(3)


def test_m():
    print("ahaa2")