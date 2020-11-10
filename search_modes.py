import elastic_func
from sklearn import preprocessing
import numpy as np


def my_score_a(movie):

    values = movie.values[2:]
    values = [values for values in values if str(values) != 'nan']

    return {**movie, "Final Score" : np.mean(values)}


def private(title, es, index, n):
    """

    Returns a shorted Dataframe of the resuluts using only BM25 metric

    """

    results = elastic_func.search_to_dataframe(es, index, title, n)

    final_results = results

    return final_results[["title","score"]].sort_values(by='score', ascending=False)


def basic(title, user_id, es, index, n, reviews):
    """

    Returns a shorted Dataframe of the resuluts using only BM25 metric and user reviews

    """

    results = elastic_func.search_to_dataframe(es, index, title, n)

    u_r = reviews[reviews.userId == user_id].rename(columns={"rating": "u_r"})
    m_r = reviews[reviews["movieId"].isin(results['movieId'].values)].groupby(by="movieId").mean().reset_index()[
        ["movieId", "rating"]].rename(columns={"rating": "m_r"})

    results = results.merge(u_r, how="left", on="movieId")[["title", "movieId", "score", "u_r"]]

    results = results.merge(m_r, how="left", on="movieId")[["movieId", "title", "score", "u_r", "m_r"]]


    min_max_scaler = preprocessing.MinMaxScaler()
    results[results.columns[2:]] = min_max_scaler.fit_transform(results[results.columns[2:]])


    final_results = results.apply(lambda x: my_score_a(x), result_type='expand', axis=1)

    return final_results[["title", "Final Score"]].sort_values(by='Final Score', ascending=False)


def advance(title, user_id, es, index, n, reviews, cluster_reviews, user_cluster):
    """

    Returns a shorted Dataframe of the results using complex metric

    """
    results = elastic_func.search_to_dataframe(es, index, title, n)

    u_r = reviews[reviews.userId == user_id].rename(columns={"rating": "u_r"})
    m_r = reviews[reviews["movieId"].isin(results['movieId'].values)].groupby(by="movieId").mean().reset_index()[
        ["movieId", "rating"]].rename(columns={"rating": "m_r"})

    cluster_reviews.index = cluster_reviews['class']
    c_r = cluster_reviews.drop(columns=['class']).T.reset_index().rename(columns={"index": "movieId",
                                                                                  user_cluster: "c_r"})
    c_r['movieId'] = c_r['movieId'].astype('int64')

    results = results.merge(u_r, how="left", on="movieId")[["title", "movieId", "score", "u_r"]]

    results = results.merge(m_r, how="left", on="movieId")[["movieId", "title", "score", "u_r", "m_r"]]

    results = results.merge(c_r[["movieId", "c_r"]], on='movieId', how='left')


    min_max_scaler = preprocessing.MinMaxScaler()
    results[results.columns[2:]] = min_max_scaler.fit_transform(results[results.columns[2:]])


    final_results = results.apply(lambda x: my_score_a(x), result_type='expand', axis=1)

    return final_results[["title", "Final Score"]].sort_values(by='Final Score', ascending=False)


def cambridge_analytica(title, user_id, es, index, n, reviews, cluster_reviews, user_cluster, predictions):
    """

    Returns a shorted Dataframe of the results using complex metric

    """
    print(user_cluster)
    results = elastic_func.search_to_dataframe(es, index, title, n)

    u_r = reviews[reviews.userId == user_id].rename(columns={"rating": "u_r"})
    m_r = reviews[reviews["movieId"].isin(results['movieId'].values)].groupby(by="movieId").mean().reset_index()[
        ["movieId", "rating"]].rename(columns={"rating": "m_r"})

    cluster_reviews.index = cluster_reviews['class']
    c_r = cluster_reviews.drop(columns=['class']).T.reset_index().rename(columns={"index": "movieId",
                                                                                  user_cluster: "c_r"})
    c_r['movieId'] = c_r['movieId'].astype('int64')

    predictions.index = predictions["userId"]
    p_r = predictions.drop(columns=['userId']).T.reset_index().rename(columns={"index": "movieId", user_id: "p_r"})
    p_r['movieId'] = p_r['movieId'].astype('int64')
    p_r['p_r'] = p_r['p_r'].apply(lambda x: int(x) / 2)

    results = results.merge(u_r, how="left", on="movieId")[["title", "movieId", "score", "u_r"]]

    results = results.merge(m_r, how="left", on="movieId")[["movieId", "title", "score", "u_r", "m_r"]]

    results = results.merge(c_r[["movieId", "c_r"]], on='movieId', how='left')

    results = results.merge(p_r[["movieId", "p_r"]], on='movieId', how='left')

    min_max_scaler = preprocessing.MinMaxScaler()
    results[results.columns[2:]] = min_max_scaler.fit_transform(results[results.columns[2:]])

    final_results = results.apply(lambda x: my_score_a(x), result_type='expand', axis=1)

    return final_results[["title", "Final Score"]].sort_values(by='Final Score', ascending=False)
