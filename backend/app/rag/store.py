from langchain_core.documents import Document
from langchain_qdrant import Qdrant

from app.rag.embeddings import embeddings


def store_chunks(chunks, video_id):

    docs = []

    for idx, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "video_id": video_id,
                    "chunk_id": idx
                }
            )
        )

    vectorstore = Qdrant.from_documents(
        docs,
        embeddings,
        location=":memory:",
        collection_name="video_chunks"
    )

    return vectorstore