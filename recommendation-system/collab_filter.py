import pandas as pd
from create_df import ratings as ra

item_similiary_df = []


def get_similiar_movs(movie_id, user_rating):
    similiar_score = item_similiary_df[movie_id]*(user_rating-2.5)
    similiar_score = similiar_score.sort_values(ascending=False)
    return similiar_score


def collab_filter(favMovies):

    tempMovies = []
    for movie in favMovies:
        tempMovies.append((movie[1], movie[2]))
    #(id, rating)
    favMovies = tempMovies

    ratings = ra
    user_ratings = ratings.pivot_table(index=['userId'], columns=[
                                       'productId'], values='rating')

    print('lol')
    print(user_ratings)
    # removing Nans
    user_ratings = user_ratings.fillna(0)
    print(user_ratings)

    # using inbuilt pierson correlation
    global item_similiary_df
    item_similiary_df = user_ratings.corr(
        method='pearson')  # the similiary matrix

    print(item_similiary_df)

    #favMovies = [("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)", 5)]

    similiar_movies = pd.DataFrame()

    for movieId, rating in favMovies:
        similiar_movies = similiar_movies.append(
            get_similiar_movs(movieId, rating), ignore_index=True)

    similiar_movies.sum().sort_values(ascending=False)
    print(similiar_movies)
    return similiar_movies


#collab_filter([("Wayona Nylon Braided USB to Lightning Fast Charging and Data Sync Cable Compatible for iPhone 13, 12,11, X, 8, 7, 6, 5, iPad Air, Pro, Mini (3 FT Pack of 1, Grey)", 0, 2)])

