import os
import re
import ssl
import time
import urllib.request
from decimal import Decimal

from bs4 import BeautifulSoup

from master.models import Brand, Product, Smartphone, Store
from master.search.indexer import index_products

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


BASE_URLS = {
    'mediamarkt': 'https://www.mediamarkt.es/es/category/smartphones-263.html',
    'phonehouse': 'https://www.phonehouse.es/moviles-y-telefonia/moviles/todos-los-smartphones.html',
    'backmarket': 'https://www.backmarket.es/es-es/l/smartphoness/6c290010-c0c2-47a4-b68a-ac2ec2b64dca',
}

def scrap_data(shop: str) -> None:
    match shop:
        case 'mediamarkt':
            fetch_mediamarkt()
        case 'phonehouse':
            fetch_phonehouse()
        case 'backmarket':
            fetch_backmarket()
        case 'all':
            fetch_mediamarkt()
            fetch_phonehouse()
            fetch_backmarket()
        case _:
            raise ValueError(f"Invalid parameter: {shop}")
        
    try:
        index_products()
    except Exception as e:
        print(f"Error indexing products: {str(e)}")        


# The num of pages can be changed, its set to 5 by default for performance.
def fetch_mediamarkt(num_pages: int = 5) -> None:
    store, created = Store.objects.get_or_create(name='MediaMarkt')
    base_url = BASE_URLS['mediamarkt']

    for i in range(1, num_pages + 1):
        req = urllib.request.Request(
            f"{base_url}?page={i}",
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept-Language': 'en-US,en;q=0.9',  # Needed to avoid 403
            },
        )
        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f, 'lxml')

        elements = soup.find_all('div', class_="sc-6877dc8f-0 fxGopN")

        for element in elements:
            try:
                content = element.find('p', class_="sc-8b815c14-0 dbwSez").text.split(",")

                name_and_brand = content[0].replace('Móvil - ', '').strip().split(' ', 1)
                brand = name_and_brand[0].upper()
                name = name_and_brand[1].capitalize()

                color = content[1].strip().capitalize() if 'GB' not in content[1] else None
                storage = _find_by_keyword(content, 'GB', exclude='RAM')
                ram = _find_by_keyword(content, 'RAM')
                screen_size = _find_by_keyword(content, '"') 
                battery = _find_by_keyword(content, 'mAh')
                
                price = _parse_price(element.find_all('span', class_="sc-e0c7d9f7-0 bPkjPs")[-1].text)

                link = "https://www.mediamarkt.es" + element.find('a', class_="sc-35c6ad71-1 dxFAqR sc-66851cef-0 dEaRKk")['href']

                brand_instance, created = Brand.objects.get_or_create(name=brand)
                smartphone_instance, created = Smartphone.objects.update_or_create(
                    name=name, brand=brand_instance, color=color,
                    storage=storage, ram=ram, screen_size=screen_size,
                    battery=battery
                )
                product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

                if product_instance:
                    product_instance.price = price
                    product_instance.link = link
                    product_instance.refurbished = False
                    product_instance.save()
                else:
                    Product.objects.create(
                        smartphone=smartphone_instance, store=store,
                        price=price, link=link, refurbished=False
                    )
                
            except Exception as e:
                print(f"Error: {e} while processing item.")
                continue
                

def fetch_phonehouse() -> None:
    store, created = Store.objects.get_or_create(name='PhoneHouse')

    base_url = BASE_URLS['phonehouse']
    req = urllib.request.Request(base_url) 
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, 'lxml')
    elements =  soup.find_all('div', class_="item-listado-final")

    for element in elements:
        try:
            color = element.find('h3', class_="marca-item").text.split(" ")[-1].capitalize()

            price = _parse_price(element.find("span", class_="precio precio-2").text)
            link = "https://www.phonehouse.es" + element.a['href']
            
            req = urllib.request.Request(link) 
            f = urllib.request.urlopen(req)
            soup = BeautifulSoup(f, 'lxml')

            name_and_brand = soup.find("div", class_="buy-box-1").find_next('h1').text
            name_and_brand = _clean_smartphone_data(name_and_brand)
            brand = name_and_brand.split(' ')[0].upper()
            name = " ".join(name_and_brand.split(' ')[1:]).capitalize()
            
            storage = int(soup.find("div", text="Memoria Interna").find_next_sibling("div").text.replace('GB', '').replace('MB', ''))
            screen_size = Decimal(soup.find("div", text="Tamaño de pantalla").find_next_sibling("div").text[:3])

            try:
                ram = int(soup.find("div", text="Memoria RAM").find_next_sibling("div").text.replace('GB', '').replace('MB', ''))
            except:
                ram = None                
            
            try:
                battery = int(soup.find("div", text="Capacidad batería").find_next_sibling("div").text.replace('mAh', ''))
            except:
                battery = None                
            
            brand_instance, created = Brand.objects.get_or_create(name=brand)
            smartphone_instance, created = Smartphone.objects.get_or_create(name=name, brand=brand_instance, color=color, 
                                                                                storage=storage, ram=ram, screen_size=screen_size, 
                                                                                battery=battery)
            product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

            if product_instance:
                product_instance.price = price
                product_instance.link = link
                product_instance.refurbished = False
                product_instance.save()
            else:
                Product.objects.create(smartphone=smartphone_instance, store=store, price=price, link=link, refurbished=False)

        except Exception as e:
            print(f"Error: {e} while processing item.")
            continue
    
def fetch_backmarket():
    store, created = Store.objects.get_or_create(name='BackMarket')

    base_url = BASE_URLS['backmarket']
    req = urllib.request.Request(
                            base_url, 
                            headers={
                                'User-Agent': 'Mozilla/5.0',
                                'Accept-Language': 'en-US,en;q=0.9',  # Needed to avoid 403
                            }) 
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f, 'lxml')
    elements = soup.find('main', class_="w-full").find_all_next("a")
    
    for element in elements:
        try:
            name = element.find("span", class_="body-1-bold line-clamp-2").text

            try:
                price = soup.find("div", class_="text-static-default-hi body-2-bold").text.replace("€", "").replace(",", ".").strip()
            except:
                price = None

            try:
                link = element['href'] if 'https://www.backmarket.es' in element['href'] else "https://www.backmarket.es" + element['href']
                req = urllib.request.Request(
                                        link, 
                                        headers={
                                            'User-Agent': 'Mozilla/5.0',
                                            'Accept-Language': 'en-US,en;q=0.9',  # Needed to avoid 403
                                        }) 
                f = urllib.request.urlopen(req)
                soup = BeautifulSoup(f, 'lxml')
                

                title = soup.title.text.split(" - ")
                storage = _clean_value(title[0].split(" ")[-1], "GB")
                color = title[1]

            except:
                title, storage, color = None, None, None
                
            
            smartphone_instance, created = Smartphone.objects.get_or_create(name=name, brand=None, color=color, 
                                                                                storage=storage, ram=None, screen_size=None, 
                                                                                battery=None)
            product_instance = Product.objects.filter(smartphone=smartphone_instance, store=store).first()

            if product_instance:
                product_instance.price = price
                product_instance.link = link
                product_instance.refurbished = True
                product_instance.save()
            else:
                Product.objects.create(smartphone=smartphone_instance, store=store, price=price, link=link, refurbished=True)
        
        except Exception as e:
            print(f"Error: {e} while processing item.")
            continue
        
        
def _find_by_keyword(content, keyword, exclude=None):
    for item in content:
        if keyword in item and (exclude is None or exclude not in item):
            return _clean_value(item, keyword)
    return None

def _clean_value(item, keyword):
    try:
        if '"' in keyword:  
            return Decimal(item.strip().split('"')[0])
        if 'mAh' in keyword or 'GB' in keyword or 'RAM' in keyword:
            return int(item.strip().replace(keyword, '').replace('GB', '').strip())
    except ValueError:
        pass
    return item.strip()  
    
def _parse_price(price_str: str) -> Decimal:
    price_str = price_str.replace('€', '').strip()
    price_str = price_str.replace(',', '.')
    return Decimal(price_str)
    
def _clean_smartphone_data(data: str) -> str:
    data = re.sub(r"\b(4G|5G)\b", "", data)
    data = re.sub(r"\b\d+GB(\+\d+GB)? RAM\b", "", data)
    data = re.sub(r"\b\d+GB\b", "", data)
    data = re.sub(r"(?:\b[a-zA-Záéíóúñ]+\b(?:\s\b[a-zA-Záéíóúñ]+\b)?$)", "", data)
    data = re.sub(r"\s{2,}", " ", data).strip()
    return data
