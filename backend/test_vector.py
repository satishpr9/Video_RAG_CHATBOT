from app.rag.store import store_chunks

chunks = [
    "Video A talks about AI.",
    "Video A discusses startups.",
    "Video B discusses politics."
]

db = store_chunks(
    chunks,
    "A"
)

print("Stored successfully")