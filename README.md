# movie-recommender
Recommender system using collaborative filtering to recommend what movie to watch next. This
recommender is based on the [MovieLens 100k dataset](https://grouplens.org/datasets/movielens/100k/).
I used [this tutorial](https://realpython.com/build-recommendation-engine-collaborative-filtering/) 
as a guide. Steps:

1. Get a dataset of items x users.
2. Based on (1), create a user correlation matrix (user x user, with values equal to the Pearson 
Correlation coefficients (R2)).
3. Given a user, use this matrix to look up the n most similar users (highest R2) who have watched
at least m movies unwatched by this user.
4. Compute predicted user ratings for each unseen movie as a weighted average of top similar users
ratings (weighted by similarity score (R2) of each top user to the user of interest).
5. Return top rated films as recommendations.

## Usage
First download the MovieLens 100k dataset from https://grouplens.org/datasets/movielens/100k/, then
unzip the contents and copy to the `datasets/` directory.

Run `python recommender.py <USER_ID>`, where `<USER_ID>` is a user id from the MovieLens 100k dataset.

## Example recommendation
You liked: 
         score                                       item_name
item_id                                                       
1          5.0                                Toy Story (1995)
178        5.0                             12 Angry Men (1957)
165        5.0                         Jean de Florette (1986)
166        5.0  Manon of the Spring (Manon des sources) (1986)
168        5.0          Monty Python and the Holy Grail (1974)
169        5.0                      Wrong Trousers, The (1993)
170        5.0                          Cinema Paradiso (1988)
171        5.0                             Delicatessen (1991)
172        5.0                 Empire Strikes Back, The (1980)
173        5.0                      Princess Bride, The (1987)
I recommend: 
         score                               item_name
item_id                                               
515        5.0                        Boot, Das (1981)
487        5.0                    Roman Holiday (1953)
522        5.0                      Down by Law (1986)
315        5.0                        Apt Pupil (1998)
316        5.0               As Good As It Gets (1997)
357        5.0  One Flew Over the Cuckoo's Nest (1975)
525        5.0                   Big Sleep, The (1946)
538        5.0                        Anastasia (1997)
432        5.0                         Fantasia (1940)
854        5.0                        Bad Taste (1987)