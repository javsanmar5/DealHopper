import os
import shutil
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, DATETIME
from whoosh.index import create_in
from datetime import datetime

def store_data():
    schema = Schema(
        name=TEXT(stored=True),
        brand=KEYWORD(stored=True),
        price=NUMERIC(stored=True, decimal_places=2),
        shop=KEYWORD(stored=True),
        last_updated=DATETIME(stored=True),
    )

    index_dir = "whoosh_index"
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.mkdir(index_dir)

    ix = create_in(index_dir, schema=schema)
    writer = ix.writer()

    # TODO: Fetch data from scrapping module
    data = fetch_smartphone_data()  
    
    for item in data:
        writer.add_document(
            name=item['name'],
            brand=item['brand'],
            price=item['price'],
            shop=item['shop'],
            last_updated=datetime.now(),
        )

    writer.commit()
    print(f"Indexing complete. Indexed {len(data)} items.")

def fetch_smartphone_data():
    # Example placeholder function
    return [
        {"name": "Phone A", "brand": "BrandX", "price": 299.99, "shop": "Shop1"},
        {"name": "Phone B", "brand": "BrandY", "price": 499.99, "shop": "Shop2"},
    ]
