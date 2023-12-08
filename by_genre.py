import pandas as pd
import numpy as np
import streamlit as st

movies_with_ratings_count = pd.read_csv("data/movies_with_ratings_count.csv")


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
