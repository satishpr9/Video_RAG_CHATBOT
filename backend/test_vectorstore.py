import app.rag.state as state

if state.VECTORSTORE:
    print("VectorStore Loaded")
else:
    print("VectorStore Missing")