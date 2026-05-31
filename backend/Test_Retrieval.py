from app.rag.store import store_chunks
from app.rag.retriever import get_retriever

chunks = [
    "AI startups are growing rapidly.",
    "Instagram reels get engagement.",
    "Hooks matter in videos."
]

db = store_chunks(chunks, "A")

retriever = get_retriever(db)

docs = retriever.invoke(
    "What improves engagement?"
)

for d in docs:
    print(d.page_content)