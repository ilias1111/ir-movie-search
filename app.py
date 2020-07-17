import streamlit as st
import search_modes
import time
from elasticsearch import Elasticsearch
import configparser
import elastic_func

MODES = ["Private", "Basic", "Advance", "Galactic"]
INDEX = "movies_test"
# Configuration

config = configparser.ConfigParser()
config.read('settings.ini')


# Initiate ElasticSearch connection

es = Elasticsearch([{'host': config["ES"]["host"], 'port': config["ES"]["port"]}])


# sidebar
private = st.sidebar.radio(
    "Private Mode",
    ("On", "Off")
)

if private == "Off":

    id = st.sidebar.text_input("Your ID")

if 1 == 1:

    st.sidebar.markdown("Preprocessing OK")

elif 1 == 0:

    st.sidebar.markdown("Preprocessing NOT OK")


if st.sidebar.button('Reset'):

    with st.spinner('Wait for it...'):

        time.sleep(5)
    st.sidebar.success('Done!')



title = st.text_input('Movie title', 'Toy Story')

if private == "Off":

    st_ms = st.radio("Mode", MODES)

else:

    st_ms = st.radio("Mode", [MODES[0]])

if st.button('Go'):

    if st_ms == MODES[0]:

        results = elastic_func.search_to_dataframe(es, INDEX, title, 30)
        st.dataframe(results)

    elif st_ms == MODES[1]:

        st.write(MODES[1])

    elif st_ms == MODES[2]:

        st.write(MODES[2])

    elif st_ms == MODES[3]:

        st.write(MODES[3])


