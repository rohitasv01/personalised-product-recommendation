import pandas as pd
import numpy as np


df = pd.read_csv("data.csv")
df['index'] = ''
i = 0
for d in range(len(df)):
    df['index'][d] = i
    i += 1
print(df.columns)

print(df.iloc[[0]]['product_name'])

users_dict = {}


ratings = pd.DataFrame(columns=['userId', 'productId', 'rating'])
i = 0
j = 0
for ind in df['index']:
    row = df[df['index'] == ind]
    rating = row['rating'].iloc[0]
    if rating == '|':
        rating = 4
    else:
        rating = float(rating)
    users = row['user_id'].iloc[0].split(',')

    for user in users:
        u = j
        if users_dict.get(user) != None:

            u = users_dict[user]
        else:
            u = j
            users_dict[user] = j
            j += 1

        ratings.loc[i] = {'userId': u, 'productId': ind, 'rating': rating}
        i += 1

print(ratings)
