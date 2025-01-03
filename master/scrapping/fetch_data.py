import os
import re
import ssl
import time
import urllib.request
from decimal import Decimal

from bs4 import BeautifulSoup

from master.models import Brand, Product, Smartphone, Store

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


BASE_URLS = {
    'mediamarkt': 'https://www.mediamarkt.es/es/category/smartphones-263.html',
    'phonehouse': 'https://www.phonehouse.es/moviles-y-telefonia/moviles/todos-los-smartphones.html',
    'backmarket': 'https://www.backmarket.es/es-es/l/smartphoness/6c290010-c0c2-47a4-b68a-ac2ec2b64dca',
    'cleverbuy': 'https://www.cleverbuy.es/smartphones/',
}

def scrap_data(shop: str) -> None:
    match shop:
        case 'mediamarkt':
            fetch_mediamarkt()
        case 'phonehouse':
            fetch_phonehouse()
        case 'backmarket':
            fetch_backmarket()
        case 'cleverbuy':
            fetch_cleverbuy()
        case _:
            fetch_mediamarkt()
            fetch_phonehouse()
            fetch_cleverbuy()
            fetch_backmarket()
            

# The num of pages can be changed, its set to 5 by default for performance.
def fetch_mediamarkt(num_pages: int = 5) -> None:

    store, created = Store.objects.get_or_create(name='MediaMarkt')

    base_url = BASE_URLS['mediamarkt']
    for i in range(1, num_pages + 1):
        req = urllib.request.Request(f"{base_url}?page={i}", 
                                     headers={
                                         'User-Agent': 'Mozilla/5.0',
                                         'Accept-Language': 'en-US,en;q=0.9', # Needed to avoid 403
                                        })
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, 'lxml')

        elements =  soup.find_all('div', class_="sc-6877dc8f-0 fxGopN")

        for element in elements:
            name_and_brand = element.find('p', class_="sc-8b815c14-0 dbwSez").text.split(",")[0]
            if 'Móvil - ' in name_and_brand:
                name_and_brand = name_and_brand.replace('Móvil - ', '')
            name_and_brand = name_and_brand.split(' ')
            brand = name_and_brand[0].upper()
            name = " ".join(name_and_brand[1:])
            price = _parse_price(element.find('span', class_="sc-e0c7d9f7-0 bPkjPs").text)
            link = "https://www.mediamarkt.es" + element.find('a', class_="sc-2fa46f1d-1 hHoKle sc-66851cef-0 dEaRKk")['href']

            brand_instance, created = Brand.objects.get_or_create(name=brand)
            smartphone_instance, created = Smartphone.objects.get_or_create(name=name, brand=brand_instance)
            product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

            if product_instance:
                product_instance.price = price
                product_instance.link = link
                product_instance.refurbished = False
                product_instance.save()
            else:
                Product.objects.create(smartphone=smartphone_instance, store=store, price=price, link=link, refurbished=False)


def fetch_phonehouse() -> None:
    store, created = Store.objects.get_or_create(name='MediaMarkt')

    base_url = BASE_URLS['phonehouse']
    req = urllib.request.Request(base_url) 
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, 'lxml')

    elements =  soup.find_all('div', class_="item-listado-final")

    for element in elements:

        name_and_brand = element.find('h3', class_="marca-item").text
        name_and_brand = _clean_smartphone_data(name_and_brand)
        
        brand = name_and_brand.split(' ')[0].upper()
        name = " ".join(name_and_brand.split(' ')[1:])
        price = _parse_price(element.find("span", class_="precio precio-2").text)
        link = "https://www.phonehouse.es" + element.a['href']
        
        brand_instance, created = Brand.objects.get_or_create(name=brand)
        smartphone_instance, created = Smartphone.objects.get_or_create(name=name, brand=brand_instance)
        product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

        if product_instance:
            product_instance.price = price
            product_instance.link = link
            product_instance.refurbished = False
            product_instance.save()
        else:
            Product.objects.create(smartphone=smartphone_instance, store=store, price=price, link=link, refurbished=False)


    
# TODO: Implement the fetch functions for the rest
def fetch_backmarket():
    ...
def fetch_cleverbuy():
    ...

    
def _parse_price(price_str: str) -> Decimal:
    price_str = price_str.replace('€', '').strip()
    price_str = price_str.replace(',', '.')
    return Decimal(price_str)
    
def _clean_smartphone_data(data: str) -> str:
    data = re.sub(r"\b(4G|5G)\b", "", data)
    data = re.sub(r"\b\d+GB(\+\d+GB)? RAM\b", "", data)
    data = re.sub(r"(?:\b[a-zA-Záéíóúñ]+\b(?:\s\b[a-zA-Záéíóúñ]+\b)?$)", "", data)
    data = re.sub(r"\s{2,}", " ", data).strip()
    return data