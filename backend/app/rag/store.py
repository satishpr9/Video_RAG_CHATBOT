from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from app.rag.embeddings import embeddings
import os

PERSIST_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")

def create_vectorstore():

    return Chroma(
        collection_name="video_rag",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR
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
        print("Warning: No chunks generated. Transcript may be empty. Skipping add.")
        return vectorstore
    vectorstore.add_documents(docs)
    print("Chunks Count:", len(chunks))
    print("Chunks:", chunks[:2])
    return vectorstore
