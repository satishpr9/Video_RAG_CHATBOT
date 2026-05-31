from app.rag.store import store_chunks
from app.rag.rag_chain import create_chain

chunks = [
    "Video A uses curiosity and emotional storytelling.",
    "Video B starts slowly and lacks a hook."
]

db = store_chunks(chunks, "A")

retriever = db.as_retriever()

chain = create_chain(retriever)

answer = chain.invoke(
    "Why did Video A perform better?"
)

print(answer)