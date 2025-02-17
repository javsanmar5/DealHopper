import os

from whoosh.fields import BOOLEAN, ID, NUMERIC, TEXT, Schema
from whoosh.index import create_in, open_dir

from master.models import Product

def _create_product_index():
    schema = Schema(
        unique_id=ID(stored=True, unique=True),
        smartphone_name=TEXT(stored=True),
        smartphone_brand=TEXT(stored=True),
        smartphone_color=TEXT(stored=True),
        smartphone_storage=NUMERIC(stored=True),
        smartphone_ram=NUMERIC(stored=True),
        smartphone_screen_size=NUMERIC(stored=True, decimal_places=2),
        smartphone_battery=NUMERIC(stored=True),
        store_name=TEXT(stored=True),
        price=NUMERIC(stored=True, decimal_places=2),
        link=ID(stored=True),
        refurbished=BOOLEAN(stored=True),
    )
    index_dir = "indexdir"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        create_in(index_dir, schema)
    return open_dir(index_dir)



def index_products():
    ix = _create_product_index()
    writer = ix.writer()

    # The select_related method is used to avoid the N+1 query problem. IMPORTANT
    for product in Product.objects.select_related('smartphone__brand').all():
        smartphone = product.smartphone
        unique_id = f"{smartphone.name}_{product.store.name}"
        writer.delete_by_term('unique_id', unique_id)

        writer.add_document(
            unique_id=unique_id,
            smartphone_name=smartphone.name,
            smartphone_brand=smartphone.brand.name if smartphone.brand else "",
            smartphone_color=smartphone.color if smartphone.color else "",
            smartphone_storage=smartphone.storage if smartphone.storage is not None else 0,
            smartphone_ram=smartphone.ram if smartphone.ram is not None else 0,
            smartphone_screen_size=smartphone.screen_size if smartphone.screen_size is not None else 0.0,
            smartphone_battery=smartphone.battery if smartphone.battery is not None else 0,
            store_name=product.store.name,
            price=product.price if product.price is not None else 0.0,
            link=product.link if product.link else "",
            refurbished=product.refurbished,
        )
    writer.commit()

