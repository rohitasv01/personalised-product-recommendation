from create_df import df
products = df


def relevance_score(product, query_tokens):
    rel_score = (sum(1 for token in query_tokens if token in str(product['product_name']).lower()) +
                 sum(1 for token in query_tokens if token in str(product['category']).lower()) +
                 sum(1 for token in query_tokens if token in str(product['about_product']).lower()) +
                 sum(1 for token in query_tokens if token in str(product['review_title']).lower()) +
                 sum(1 for token in query_tokens if token in str(product['review_content']).lower()))
    return rel_score


def rank_products(search_query):
    query_tokens = search_query.lower().split()

    products['relevance_score'] = products.apply(
        lambda row: relevance_score(row, query_tokens), axis=1)
    sorted_products = products.sort_values(
        by='relevance_score', ascending=False)
    return sorted_products


def searchQuery(search_query):

    search_results = rank_products(search_query)
    print(search_results.columns)
    return search_results
  

print(searchQuery('head'))
