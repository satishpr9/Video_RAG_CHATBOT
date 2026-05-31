def build_retriever(store):

    return store.as_retriever(
        search_kwargs={
            "k":4
        }
    )