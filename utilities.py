import pandas as pd
import numpy as np
import streamlit as st

movies_with_ratings_count = pd.read_csv("data/movies_with_ratings_count.csv")

similarity_top_30 = pd.read_csv("data/similarity_top_30.csv")


@st.cache_data
def top_movies_in_genre(genre, df=movies_with_ratings_count, n=10) -> pd.DataFrame:
    """
    Returns the top n movies in a genre
    """

    # Filter DataFrame for rows with the specified genre
    genre_df = df[df["genres"].str.contains(genre)]

    # Sort DataFrame by count in descending order
    sorted_genre_df = genre_df.sort_values(by="count", ascending=False)

    # Take the top n rows
    top_movies = sorted_genre_df.head(n)

    return top_movies


def get_random_movies(n=1, excludeList=None):
    """
    Returns n random movies, excluding movie_ids in the exclude list
    """
    # Get the number of movies
    num_movies = movies_with_ratings_count.shape[0]

    # Generate n random movie_ids
    random_movie_ids = np.random.randint(1, num_movies, n)

    # If excludeList is not None, remove movie_ids in excludeList from random_movie_ids
    if excludeList is not None:
        random_movie_ids = [
            movie_id for movie_id in random_movie_ids if movie_id not in excludeList
        ]

    while excludeList is not None and len(random_movie_ids) < n:
        # If excludeList is not None and the length of random_movie_ids is less than n,
        # generate more random movie_ids and append to random_movie_ids
        random_movie_ids += get_random_movies(
            n - len(random_movie_ids), excludeList=random_movie_ids
        )

    # Get the movies corresponding to the random_movie_ids
    random_movies = movies_with_ratings_count[
        movies_with_ratings_count["movie_id"].isin(random_movie_ids)
    ]

    return random_movies


@st.cache_data
def myIBCF(newuser, similarity_matrix=similarity_top_30):
    # Get all movie keys from the similarity matrix
    movie_keys = similarity_matrix.keys()

    # newuser is a dataframe with movie_ids as index and ratings as values
    # For any key not in newuser, set the value to NaN
    for key in movie_keys:
        if key not in newuser.index:
            newuser[key] = np.nan

    not_rated_indices = []
    for index in newuser.index:
        if np.isnan(newuser[index]):
            not_rated_indices.append(index)
    df_not_rated = pd.DataFrame(index=not_rated_indices, columns=["Value"])

    for l in df_not_rated.index:
        Sl = S_top30.loc[l].dropna()

        movie_score_num = 0
        movie_score_denom = 0
        w = newuser

        for i in Sl.index:
            if np.isnan(w[i]):
                w_i = 0
            else:
                w_i = w[i]
            movie_score_num += w_i * Sl[i]
            if w_i != 0:
                movie_score_denom += Sl[i]
        if movie_score_denom != 0:
            df_not_rated.loc[l] = movie_score_num / movie_score_denom

    return df_not_rated.sort_values(by="Value", ascending=False).head(10)