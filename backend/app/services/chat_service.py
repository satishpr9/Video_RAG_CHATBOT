import app.rag.state as state

from app.rag.rag_chain import create_chain

def ask_question(question):

    if state.VECTORSTORE is None:

        return {
            "error":
            "Please ingest videos first."
        }

    retriever = state.VECTORSTORE.as_retriever(
        search_kwargs={
            "k": 5
        }
    )

    docs = retriever.invoke(question)

    chain = create_chain(retriever)

    answer = chain.invoke(question)

    sources = []

    for doc in docs:

        sources.append(
            {
                "video_id":
                    doc.metadata.get("video_id"),

                "chunk_id":
                    doc.metadata.get("chunk_id")
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }