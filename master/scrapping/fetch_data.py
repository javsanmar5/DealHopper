import os
import ssl
import urllib.request

from bs4 import BeautifulSoup

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


BASE_URLS = {
    'mediamarkt': 'https://www.mediamarkt.es/es/category/smartphones-263.html',
    'pccomponentes': 'https://www.pccomponentes.com/smartphone-moviles',
    'phonehouse': 'https://www.phonehouse.es/moviles-y-telefonia/moviles/todos-los-smartphones.html',
}

