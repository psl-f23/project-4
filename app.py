"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

from by_genre import top_movies_in_genre


def main():
    st.title("Project 4: Movie Recommender")

    with st.sidebar:
        st.header("Recommender Type")
        recommender_options = ("Recommendations by Genre", "Recommendations by Ratings")
        selected_recommender = st.selectbox(
            "Select a type of recommendation", recommender_options
        )

    if selected_recommender == "Recommendations by Genre":
        st.header("Recommendations by Genre")

        # Get genre options from genres.csv
        genre_options = pd.read_csv("data/genres.csv")["Genre"].to_list()
        selected_genre = st.selectbox(
            "Movie Genre", genre_options, None, placeholder="Select a movie genre"
        )

        # Predefined top n movies in genre option
        top_n_options = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50)
        selected_top_n = st.selectbox(
            "Number of Recommendations",
            top_n_options,
            1,
            format_func=lambda x: f"{x} movies",
        )

        if st.button(
            "Get Recommendations",
            disabled=selected_genre is None or selected_top_n is None,
        ):
            st.write(f"Getting the top {selected_top_n} movies in {selected_genre}")
            top_movies = top_movies_in_genre(selected_genre, n=selected_top_n)
            st.write(top_movies)

    elif selected_recommender == "Recommendations by Ratings":
        st.header("Recommendations by Ratings")
        st.write("This is the recommendations by ratings page")


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
