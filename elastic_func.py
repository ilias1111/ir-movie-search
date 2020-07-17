from elasticsearch import Elasticsearch
import pandas as pd


def check_if_index_exists(es, index_name):

    return es.indices.exists(index=index_name)


def index_dataframe_data(es, index_mame, df):

    for i in df.values:

        es.index(index=index_mame, body={**dict(zip(df.columns, i))})


def search_to_dataframe(es, index_name, query, n_size):

    results = es.search(index=index_name, body={"query": {"match": {'title': query}}}, size=n_size)

    return pd.DataFrame([{**{"score": result["_score"]}, **result["_source"]} for result in results["hits"]["hits"]])
