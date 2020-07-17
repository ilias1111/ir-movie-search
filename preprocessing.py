import pandas as pd
import os


def check_preprocessing_directory():

    pass


def check_preprocessing_files():

    pass


def load_init_data():

    movies = pd.read_csv("./data/movies.csv")
    ratings = pd.read_csv("./data/ratings.csv")

    return movies, ratings
