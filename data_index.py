from elasticsearch import Elasticsearch
import pandas as pd
import re
import configparser


def production_year_extract(text):
    results = re.findall('\([0-9]{4,4}\)', text)

    if len(results) == 1:

        return int(results[0][1:-1])

    else:

        return pd.NA



movies = pd.read_csv("./data/movies.csv")
reviews = pd.read_csv("./data/ratings.csv")

movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))
movies["year"] = movies["title"].apply(lambda x: production_year_extract(x))


config = configparser.ConfigParser()
config.read('settings.ini')


# Initiate ElasticSearch connection

es = Elasticsearch([{'host': config["ES"]["host"], 'port': config["ES"]["port"]}])


def index_movies(movies, es, index_name):

    for i in movies.values:
        es.index(index="index_name", body={**dict(zip(movies.columns, i))})
