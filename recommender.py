import pandas as pd
import sys

# CONSTANTS
NR_UNWATCHED_MOVIES_WATCHED = 50
TOP_N_SIMILAR = 10

# Read in movie-user data
data = pd.read_csv(
    "datasets/ml-100k/u.data",
    sep="\t", 
    names=["user_id", "item_id", "rating", "timestamp"]
)

# Movie metadata (names etc)
item_attr = pd.read_csv(
    "datasets/ml-100k/u.item",
    sep="|",
    usecols=[0, 1],
    names=["item_id", "item_name"],
    encoding = "ISO-8859-1"
)

# Select relevant columns
data = data[["user_id", "item_id", "rating"]]

# Pivot data into item x user
data = data.pivot(index="item_id", columns="user_id", values="rating")

# Read in user
user = int(sys.argv[1])

# Find users top movies for comparison
user_top = data[user][lambda x: x>0].sort_values(ascending=False).head(10)

s2 = user_top.to_frame().rename(columns={user: "score"})
s1 = item_attr.set_index("item_id")
user_top_movies = pd.merge(s2 , s1, how="left", left_index=True, right_index=True)
print("You liked: ")
print(user_top_movies.sort_values("score", ascending=False))

# Find all movies not watched by user
unwatched = set(data[user][lambda x: x.isna()].index)

# Find all users that watched at least NR_UNWATCHED_MOVIES_WATCHED of these movies
n_watched_per_user = data.loc[unwatched].count()

freq_watched_user = (
    n_watched_per_user[n_watched_per_user > NR_UNWATCHED_MOVIES_WATCHED]
    .index
    .tolist())

freq_watched_user.append(user)
needed_users = data[freq_watched_user]

# Given a user, find the similar users
# Calculate user similarity matrix
needed_users_corr = needed_users.corr()

# Find top TOP_N_SIMILAR similar users in this list
top_n_weights = (
    needed_users_corr.loc[user].sort_values(ascending=False)
    [lambda x: x.index != user]
    .head(TOP_N_SIMILAR))

# Find movies they saw (in unseen)
scores = data.loc[unwatched][top_n_weights.index]

# Calculate predicted ratings for user of unwatched movies
# as a weighted average of most similar users scores
scores_ones = scores.copy()
scores_ones[scores_ones > 0] = 1
weight_matrix = scores_ones * top_n_weights
weighted_scores = scores * top_n_weights
final_scores = weighted_scores.sum(axis=1) / weight_matrix.sum(axis=1)

# Join to find corresponding names of top recommended movies
s2 = final_scores.to_frame().rename(columns={0:"score"})
s1 = item_attr.set_index("item_id")
final = pd.merge(s2 , s1, how="left", left_index=True, right_index=True)

# Print recommendation
print("I recommend: ")
print(final.sort_values("score", ascending=False).head(10))
