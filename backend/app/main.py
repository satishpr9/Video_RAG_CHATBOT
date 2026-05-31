from fastapi import FastAPI
from app.routes.ingest import router as ingest_router
app = FastAPI()
app.include_router(ingest_router)
@app.get("/")
def home():
    return {"message": "Video RAG API"}