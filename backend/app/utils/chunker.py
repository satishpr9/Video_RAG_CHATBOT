from celery import chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    print("Generated Chunks:", len(chunks))

    return chunks