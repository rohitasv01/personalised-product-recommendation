import functools as ft
from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from create_df import df

###### helper functions. Use them when needed #######


def get_name_from_index(index):
    return df[df.index == index]["product_name"].values[0]


def get_index_from_name(product_name):
    return df[df.product_name == product_name]["index"].values[0]
##################################################


# Step 1: Read CSV File into dataframe
# df = pd.read_csv("amazon.csv")
# df['index']=''
# i = 0
# for d in range(len(df)):
#     df['index'][d] = i
#     i += 1
# print(df.columns)


# JOINING THE DFS


def content_rec(fav_movie):
    ##################################################
    # Step 2: Select Features
    features = ['category', 'product_name', 'about_product']

    for feature in features:
        df[feature] = df[feature].fillna('')  # fill all NaN with empty string

    ##################################################
    # Step 3: Create a column in DF which combines all selected features

    def combine_features(row):  # take a row from the dataset
        s = " "
        # print(s.join(row["genres"]))
        return row['category'].replace('|', ' ')+" "+row['product_name']+' '+row["about_product"]

    # creating new column in the df
    # applies the function on the df vertically(pass each row individually)
    df["combined_features"] = df.apply(combine_features, axis=1)

    ##################################################

    # Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    # for each word in the combined features of each row, we find the count(occurence) of each word in that row

    ##################################################

    # Step 5: Compute the Cosine Similarity based on the count_matrix

    # gives the similiarity scores between all the movies
    cosine_sim = cosine_similarity(count_matrix)
    # each row  represents one movie, and the columns contain the similiarity with the other movies

    ##################################################
    # INPUT MOVIE FROM USER
    movie_user_likes = fav_movie

    ##################################################
    # Step 6: Get index of this movie from its name
    movie_index = get_index_from_name(movie_user_likes)

    # gives list of (tuples) in the form [(index of movie, similiarity score)]
    similiar_movies = list(enumerate(cosine_sim[movie_index]))

    ##################################################
    # Step 7: Get a list of similar movies in descending order of similarity score
    # sorting

    sorted_similiar_movies = sorted(
        similiar_movies, key=lambda x: x[1], reverse=True)

    ##################################################
    # Step 8: Print names of first 50 movies

    i = 0

    sorted_similiar_movies_tuples = []

    for movie in sorted_similiar_movies:
        sorted_similiar_movies_tuples.append(
            (get_name_from_index(movie[0]), movie[0]))
        i = i+1
        if(i > 50):
            break

    return sorted_similiar_movies_tuples


#print(content_rec('Wayona Nylon Braided USB to Lightning Fast Charging and Data Sync Cable Compatible for iPhone 13, 12,11, X, 8, 7, 6, 5, iPad Air, Pro, Mini (3 FT Pack of 1, Grey)'))
