import wikipedia


def search_wikipedia(query):

    try:

        return wikipedia.summary(
            query,
            sentences=5
        )

    except Exception as e:

        return str(e)