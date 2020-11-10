import pandas as pd
import streamlit as st
import os



@st.cache(allow_output_mutation=True)
def load_init_data():

    movies = pd.read_csv("./data/movies.csv")
    ratings = pd.read_csv("./data/ratings.csv")

    user_class = pd.read_csv("./user_class.csv")
    cluster_average = pd.read_csv("./cluster_average.csv")

    predicted_rating = pd.read_csv("./predictions.csv")

    return movies, ratings, user_class, cluster_average, predicted_rating
