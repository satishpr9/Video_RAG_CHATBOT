# from celery import chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):

    print("Incoming text length:", len(text))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    print("Generated chunks:", len(chunks))

    return chunks