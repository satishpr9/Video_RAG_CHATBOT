from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.config import settings
import app.rag.state as state


llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)


prompt = ChatPromptTemplate.from_template("""
You are a social media analytics expert.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Use the conversation history if it is relevant.

If the answer is not available in the videos, say:
"Not found in videos."

Answer:
""")


def format_docs(docs):

    return "\n\n".join(
        f"[Video {d.metadata.get('video_id')} - Chunk {d.metadata.get('chunk_id')}]\n{d.page_content}"
        for d in docs
    )


def get_history():

    if not state.CHAT_HISTORY:
        return "No previous conversation."

    return "\n".join(
        [
            f"User: {item['question']}\nAssistant: {item['answer']}"
            for item in state.CHAT_HISTORY[-5:]
        ]
    )


def create_chain(retriever):

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "history": lambda x: get_history()
        }
        | prompt
        | llm
    )

    return chain