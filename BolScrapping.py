import time
import requests
import csv
from bs4 import BeautifulSoup as soup
import requests


electronic_url = [
    'https://www.bol.com/nl/l/smartphones/N/4010/?page=',
    'https://bol.com/nl/l/laptops/N/4770/?page='
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


def get_requests(csv_writer, url_):
    a_response_ = requests.get(url=url_,
                               headers=headers)
    time.sleep(3)
    products_ = soup(a_response_.text, "html.parser")

    products = products_.find('ul', {'class': 'list-view product-list js_multiple_basket_buttons_page'})
    # print(products)
    time.sleep(1)
    for product in products.findAll('li', {'class': 'product-item--row js_item_root'}):
        name = product.find('a', {'class': 'product-title px_list_page_product_click'})
        try:
            link_url = 'https://www.bol.com/' + name['href']
        except TypeError:
            link_url = "not found"

        # old_price = product.find('div', {'class': 'small_details product-prices'})
        discount_price = product.find('strong', {'class': 'product-prices__currency'})

        price = product.find('span', {'class': 'promo-price'})
        brand = product.find('ul', {'class': 'product-creator'})
        brand = brand.find('a')

        if name is None:
            name = "not found"
        else:
            name = name.text.strip(" ")

        if price is None:
            price = "0"
        else:
            price = price.text.strip(" ").split('.', 1)[0]
            price = price.strip(" ").split(' ', 1)[0]
            price = price.strip(" ")
            price = price.strip("\n")
            price = price.replace("\n", "")
            price = price.replace("-", "")

        if brand is None:
            brand = "not found"
        else:
            brand = brand.text.strip(" ")

        if discount_price is None:
            discount_price = '0'
        else:
            discount_price = discount_price.text.strip(" ").strip("\n")
            discount_price = discount_price.split(',', 1)[0].replace(".", "")
        if discount_price == '0':
            discount = 0
        elif price == '0':
            discount = 0
        else:
            discount = round(int(price)) - round(int(discount_price))
        # print(str(discount))
        # print("name: " + name[0:10] + "  price: " + price + "  brand: " + brand, " discount_price: " + discount_price +  " url: "+ link_url[0:10])
        csv_writer.writerow([name, price, discount_price, str(discount), brand, link_url])


def start_scrapper():
    with open('BolLaptops.csv', 'w', newline='') as laptops:
        writer_laptop = csv.writer(laptops)
        # Laptops
        for i in range(1, 4):
            print(electronic_url[1] + str(i))
            get_requests(writer_laptop, electronic_url[1] + str(i))
            time.sleep(3)

    with open('BolMobiles.csv', 'w', newline='') as mobiles:
        writer_mobiles = csv.writer(mobiles)
        # Mobiles
        for i in range(1, 4):
            print(electronic_url[0] + str(i))
            get_requests(writer_mobiles, electronic_url[0] + str(i))
            time.sleep(3)

def test_m():
    print("ahaa1")
