import os

from whoosh.fields import BOOLEAN, ID, NUMERIC, TEXT, Schema
from whoosh.index import create_in, open_dir

from master.models import Product


def _create_product_index():
    schema = Schema(
        smartphone_name=TEXT(stored=True),
        store_name=TEXT(stored=True),
        price=NUMERIC(stored=True, decimal_places=2),
        link=ID(stored=True),
        refurbished=BOOLEAN(stored=True)
    )
    index_dir = "indexdir"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        create_in(index_dir, schema)
    return open_dir(index_dir)


def index_products():
    ix = _create_product_index()
    writer = ix.writer()
    for product in Product.objects.all():
        writer.add_document(
            smartphone_name=product.smartphone.name,
            store_name=product.store.name,
            price=product.price,
            link=product.link,
            refurbished=product.refurbished
        )
    writer.commit()

