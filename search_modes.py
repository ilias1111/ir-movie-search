import elastic_func



def private(title, es, index, n):

    """

    Returns a shorted Dataframe of the resuluts using only BM25 metric

    """

    results = elastic_func.search_to_dataframe(es, index, title, n)

    final_results = results

    return final_results



def basic(title):
    """

    Returns a shorted Dataframe of the resuluts using only BM25 metric and user reviews

    """

    pass



def advance(title):
    """

    Returns a shorted Dataframe of the resuluts using complex metric

    """

    pass


def cambridge_analytica(title, id):
    """

    Returns a shorted Dataframe of the resuluts using complex metric

    """

    pass
