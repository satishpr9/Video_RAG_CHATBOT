import app.rag.state as state

from app.rag.rag_chain import create_chain
def ask_stream(question):

    retriever = state.VECTORSTORE.as_retriever(
        search_kwargs={"k": 5}
    )

    chain = create_chain(retriever)

    full_answer = ""

    for chunk in chain.stream(question):

        if hasattr(chunk, "content"):

            full_answer += chunk.content

            yield chunk.content

    state.CHAT_HISTORY.append(
        {
            "question": question,
            "answer": full_answer
        }
    )