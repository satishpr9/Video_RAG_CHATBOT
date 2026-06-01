def build_retriever(store):

    return store.as_retriever(
        search_kwargs={
            "k":4
        }
    )

def format_docs(docs):

    return "\n\n".join(
        f"""
Video: {d.metadata.get('video_id')}
Chunk: {d.metadata.get('chunk_id')}

Text:
{d.page_content}
"""
        for d in docs
    )