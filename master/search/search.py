from whoosh.qparser import QueryParser

from master.search.indexer import _create_product_index


def search_products(query):
    ix = _create_product_index()
    with ix.searcher() as searcher:
        parser = QueryParser("smartphone_name", ix.schema)
        parsed_query = parser.parse(query)
        results = searcher.search(parsed_query)
        return [
            {
                "smartphone_name": r["smartphone_name"],
                "store_name": r["store_name"],
                "price": r["price"],
                "link": r["link"],
                "refurbished": r["refurbished"],
            }
            for r in results
        ]
