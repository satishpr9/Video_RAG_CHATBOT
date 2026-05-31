from app.rag.store import store_chunks

chunks = [
    "Video A uses a strong emotional hook.",
    "Video B starts slowly."
]

db = store_chunks(chunks, "A")

retriever = db.as_retriever()

results = retriever.invoke(
    "Which video has a stronger hook?"
)

for doc in results:
    print(doc.page_content)