from fastapi import FastAPI
from app.routes.ingest import router as ingest_router
from app.routes.chat import router as chat_router
app = FastAPI()
app.include_router(ingest_router)
app.include_router(chat_router)
@app.get("/")
def home():
    return {"message": "Video RAG API"}