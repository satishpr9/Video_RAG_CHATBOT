from langchain_core.documents import Document

from app.rag.embeddings import embeddings

from langchain_qdrant import QdrantVectorStore

from app.rag.qdrant_service import client

def save_chunks(chunks, video_id):

    docs = []

    for idx, chunk in enumerate(chunks):

        docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "video_id":video_id,
                    "chunk_id":idx
                }
            )
        )

    store = QdrantVectorStore.from_documents(
        docs,
        embeddings,
        client=client,
        collection_name="video_rag"
    )

    return store