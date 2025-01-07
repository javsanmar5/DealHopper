from whoosh.qparser import MultifieldParser

from master.search.indexer import _create_product_index

def search_products(query):
    ix = _create_product_index()
    with ix.searcher() as searcher:
        parser = MultifieldParser(
            ["smartphone_name", "smartphone_brand", "smartphone_color"], 
            schema=ix.schema
        )
        parsed_query = parser.parse(query)
        results = searcher.search(parsed_query)
        return [
            {
                "smartphone_name": r["smartphone_name"],
                "smartphone_brand": r["smartphone_brand"],
                "smartphone_color": r["smartphone_color"],
                "smartphone_storage": r["smartphone_storage"],
                "smartphone_ram": r["smartphone_ram"],
                "smartphone_screen_size": r["smartphone_screen_size"],
                "smartphone_battery": r["smartphone_battery"],
                "store_name": r["store_name"],
                "price": r["price"],
                "link": r["link"],
                "refurbished": r["refurbished"],
            }
            for r in results
        ]
