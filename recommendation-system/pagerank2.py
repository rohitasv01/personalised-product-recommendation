from create_df import df
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from difflib import get_close_matches
import numpy as np
import networkx as nx

products=df

product_id_to_index = {product_id: index for index, product_id in enumerate(products['product_id'])}
index_to_product_id = {index: product_id for product_id, index in product_id_to_index.items()}

def determine_related_prod():
    products['combined_att'] = (products['product_name'] + ' ' + products['category'] + ' ' + products['about_product'] + ' ' + products['review_title'] + ' ' + products['review_content'])

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(products['combined_att'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    related_products = {}
    for idx, product_id in enumerate(products['product_id']):
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        related_products[product_id] = [products['product_id'][i] for i, score in sim_scores[1:6]]

    return related_products

def create_directed_graph():
    G = nx.DiGraph()

    for index, row in products.iterrows():
        G.add_node(product_id_to_index[row['product_id']], category=row['category'])

    for index, row in products.iterrows():
        related_products = products['related_products'].iloc[index]  
        #print(related_products)
        for related_product_id in related_products:
            if related_product_id in product_id_to_index:
                G.add_edge(product_id_to_index[row['product_id']], product_id_to_index[related_product_id])

    return G

def calc_scores(G, search_query):
    relevance_scores = {}
    for index, row in products.iterrows():
        product_description = row['about_product']
        relevance_score = calculate_relevance(search_query, product_description)  
        relevance_scores[product_id_to_index[row['product_id']]] = relevance_score

    pagerank_scores = nx.pagerank(G, alpha=0.85)  

    final_scores = {index: pagerank_scores[index] + relevance_scores.get(index, 0) for index in G.nodes}

    sorted_product_indices = sorted(final_scores, key=final_scores.get, reverse=True)

    return sorted_product_indices, final_scores

def calculate_relevance(search_query, product_description):
    search_terms = search_query.lower().split()
    description_words = product_description.lower().split()
    relevance_score = sum(description_words.count(term) for term in search_terms)
    return relevance_score



related_products = determine_related_prod()
products['related_products'] = products['product_id'].apply(lambda x: related_products.get(x,[]))


G = create_directed_graph()

def searchQuery(search_query): 
    # search_query = "pillow"

    sorted_product_indices, final_scores = calc_scores(G, search_query)

    return sorted_product_indices
    # print("Rank\tProduct ID\tDescription")
    # for rank, index in enumerate(sorted_product_indices, start=1):
    #     product_id = index_to_product_id[index]
    #     product_description = products.loc[products['product_id'] == product_id, 'about_product'].values[0]
    #     print(f"{rank}\t{product_id}\t{product_description}")


# searchQuery('pillow')




