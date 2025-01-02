import os
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
    'phone_house': 'https://www.phonehouse.es/moviles-y-telefonia/moviles/todos-los-smartphones.html',
    'mas_movil': 'https://www.masmovil.es/catalogo/telefonos-moviles',
}

def scrap_data(shop: str) -> None:
    match shop:
        case 'mediamarkt':
            _fetch_mediamarkt()
        case 'phone_house':
            _fetch_phonehouse()
        case 'mas_movil':
            _fetch_mas_movil()
        case _:
            _fetch_mas_movil()
            _fetch_phonehouse()
            _fetch_mediamarkt()
            

# TODO: Implement the fetch functions for Mas Movil
def _fetch_mas_movil() -> None:
    if not Store.objects.filter(name='MasMovil').exists():
        Store(name='MasMovil').save()
        
    base_url = BASE_URLS['mas_movil']
    req = urllib.request.Request(f"{base_url}", )
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, 'lxml')

    elements = soup.find_all('a', class_='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary')
    
    for element in elements:
        try:
            header = element.find('h2', class_="MuiTypography-root MuiTypography-h2 MuiTypography-alignCenter")
            brand = element.find('span', class_="MuiTypography-root high-emphasis uppercase MuiTypography-subtitle2").text.strip()
            name = header.text.replace(brand, '').strip()
            price = None
            
        except AttributeError:
            continue
    
# The num of pages can be changed, its set to 5 by default for performance.
def _fetch_mediamarkt(num_pages: int = 5) -> None:

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
            brand = name_and_brand[0]
            name = " ".join(name_and_brand[1:])
            price = _parse_price(element.find('span', class_="sc-e0c7d9f7-0 bPkjPs").text)
            link = f"https://www.mediamarkt.es{element.find('a', class_="sc-2fa46f1d-1 hHoKle sc-66851cef-0 dEaRKk")['href']}"

            brand_instance, created = Brand.objects.get_or_create(name=brand)
            smartphone_instance, created = Smartphone.objects.get_or_create(name=name, brand=brand_instance)
            product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

            if product_instance:
                product_instance.price = price
                product_instance.link = link
                product_instance.save()
            else:
                Product.objects.create(smartphone=smartphone_instance, store=store, price=price, link=link)


def _parse_price(price_str: str) -> Decimal:
    price_str = price_str.replace('€', '').strip()
    price_str = price_str.replace(',', '.')
    return Decimal(price_str)


# TODO: Implement the fetch functions for Mas Movil
def _fetch_phonehouse():
    ...