"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

from utilities import top_movies_in_genre, get_random_movies, myIBCF
from streamlit_extras.grid import grid


@st.cache_data
def get_movie_image(movie_id):
    """
    Returns the image of a movie given its movie_id
    """
    return f"https://liangfgithub.github.io/MovieImages/{movie_id}.jpg?raw=true"


# Initialize session states


def main():
    st.title("Project 4: Movie Recommender")

    with st.sidebar:
        # Initialize session state
        if "selected_recommender" not in st.session_state:
            st.session_state.selected_recommender = None

        st.header("Recommender Type")
        recommender_options = ("Recommendations by Genre", "Recommendations by Ratings")
        selected_recommender = st.selectbox(
            "Select a type of recommendation", recommender_options
        )
        st.session_state.selected_recommender = selected_recommender

    if st.session_state.selected_recommender == "Recommendations by Genre":
        # Initialize session states
        if "selected_genre" not in st.session_state:
            st.session_state.selected_genre = None
        if "selected_top_n" not in st.session_state:
            st.session_state.selected_top_n = None

        st.header("Recommendations by Genre")

        # Get genre options from genres.csv
        genre_options = pd.read_csv("data/genres.csv")["Genre"].to_list()
        selected_genre = st.selectbox(
            "Movie Genre", genre_options, None, placeholder="Select a movie genre"
        )
        st.session_state.selected_genre = selected_genre

        # Predefined top n movies in genre option
        top_n_options = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        selected_top_n = st.selectbox(
            "Number of Recommendations",
            top_n_options,
            1,
            format_func=lambda x: f"{x} movies",
        )
        st.session_state.selected_top_n = selected_top_n

        if st.button(
            "Get Recommendations",
            disabled=selected_genre is None or selected_top_n is None,
        ):
            st.write(f"Getting the top {selected_top_n} movies in {selected_genre}")
            top_movies = top_movies_in_genre(selected_genre, n=selected_top_n)

            # For each movie in top_movies dataframe, get the image and display it
            movie_urls = top_movies.apply(
                lambda row: get_movie_image(row["movie_id"]), axis=1
            ).to_list()

            movie_captions = top_movies.apply(
                lambda row: row["title"], axis=1
            ).to_list()

            # Define a grid
            movies_grid = grid([1, 1, 1], gap="medium")
            for movie_url, movie_caption in zip(movie_urls, movie_captions):
                movies_grid.image(movie_url, movie_caption, use_column_width=True)

    elif st.session_state.selected_recommender == "Recommendations by Ratings":
        # Infer ratings from session state, key is in format ${movie_id}-rating
        movie_ratings = {}
        for key in st.session_state.keys():
            if key.endswith("-rating"):
                movie_id = key.split("-")[0]
                movie_ratings[movie_id] = st.session_state[key]

        # movie_ratings where the value is not None
        num_rated = len(
            [rating for rating in movie_ratings.values() if rating is not None]
        )

        st.header("Recommendations by Ratings")
        if num_rated < 10:
            st.write(
                f"Please rate {10 - num_rated} more movies to get movie recommendations"
            )
        else:
            st.write(
                "You have rated 10 movies. Click the button below to get recommendations"
            )

        with st.expander(f"Movies Rated ({num_rated})", expanded=num_rated < 10):

            @st.cache_data
            def get_initial_movies():
                return get_random_movies(10)

            if "movies_to_rate" not in st.session_state:
                st.session_state.movies_to_rate = None

            if st.session_state.movies_to_rate is None:
                st.session_state.movies_to_rate = get_initial_movies()

            # Loop through each dataframe row and display the movie poster
            movies_grid = grid([1, 1], gap="medium")
            for index, movie in st.session_state.movies_to_rate.iterrows():
                # Create a container
                movie_id = movie["movie_id"]
                movie_title = movie["title"]
                movie_genres = movie["genres"]
                movie_url = get_movie_image(movie_id)

                rating_key = f"{movie_id}-rating"
                c = st.container(border=True)
                c.subheader(movie_title)

                col1, col2 = c.columns(2)
                col1.image(movie_url)
                col2.write(f"Genres: {movie_genres}")
                col2.selectbox(
                    "Rating",
                    range(1, 6),
                    None,
                    placeholder="Choose a rating",
                    key=rating_key,
                )

                if col2.button("Skip", key=f"{movie_id}-skip"):
                    new_movie = get_random_movies(1, excludeList=[movie_id])
                    st.session_state.movies_to_rate.loc[index] = new_movie.iloc[0]
                    movie_title = new_movie.iloc[0]["title"]
                    st.rerun()

        if num_rated >= 10:
            if st.button("Get Recommendations", disabled=num_rated < 10):
                st.write("Number of movies rated: ", num_rated)
                # Convert movie_ratings to a Pandas series
                user_ratings = pd.Series(movie_ratings)

                # Convert keys to m{movie_id} format
                user_ratings.index = user_ratings.index.map(lambda x: f"m{x}")
                recommendations = myIBCF(newuser=user_ratings)
                st.table(recommendations)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Movie Recommender",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            Made by
            <ul>
                <li>Baolong Truong (baolong3)</li>
                <li>Robbie Li (robbiel2)</li>
                <li>Wesley Ecoiffier (wesleye2)</li>
            </ul>
            <i>Practical Statistical Learning, Fall 2023</i>
            """,
            unsafe_allow_html=True,
        )
