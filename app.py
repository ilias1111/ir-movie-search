import streamlit as st
import search_modes
from elasticsearch import Elasticsearch
import configparser
import preprocessing

MODES = ["Private", "Basic", "Advance", "Galactic"]
INDEX = "movies_test"
# Configuration

config = configparser.ConfigParser()
config.read('settings.ini')


# Initiate ElasticSearch connection

es = Elasticsearch([{'host': config["ES"]["host"], 'port': config["ES"]["port"]}])

movies, reviews, user_class, cluster_average, predicted_rating = preprocessing.load_init_data()


# sidebar
private = st.sidebar.radio(
    "Private Mode",
    ("On", "Off")
)

if private == "Off":

    id = st.sidebar.text_input("Your ID", 1)
    u_class = user_class[user_class.userId == int(id)]['class'].values[0]



title = st.text_input('Movie title', 'Toy Story')


if private == "Off":

    st_ms = st.radio("Mode", MODES)

else:

    st_ms = st.radio("Mode", [MODES[0]])

if st.button('Go'):

    if st_ms == MODES[0]:

        results = search_modes.private(title, es, INDEX, 30)
        st.dataframe(results)

    elif st_ms == MODES[1]:

        results = search_modes.basic(title, int(id), es, INDEX, 30, reviews)
        st.dataframe(results)

    elif st_ms == MODES[2]:

        results = search_modes.advance(title, int(id), es, INDEX, 30, reviews, cluster_average, u_class)
        st.dataframe(results)

    elif st_ms == MODES[3]:

        print(u_class)
        results = search_modes.cambridge_analytica(title, int(id), es, INDEX, 30, reviews,
                                                   cluster_average, u_class, predicted_rating)
        st.dataframe(results)


