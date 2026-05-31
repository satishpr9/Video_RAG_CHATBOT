from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from app.rag.embeddings import embeddings
def create_vectorstore():

    return Chroma(
        collection_name="video_rag",
        embedding_function=embeddings
    )


def add_chunks(
    vectorstore,
    chunks,
    video_id
):

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
    print("Docs Count:", len(docs))
    if not docs:
        raise ValueError(
        "No chunks generated. Transcript may be empty."
    )
    vectorstore.add_documents(docs)
    print("Chunks Count:", len(chunks))
    print("Chunks:", chunks[:2])
    return vectorstore
