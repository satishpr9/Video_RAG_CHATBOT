from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.config import settings

llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)
prompt = ChatPromptTemplate.from_template("""
You are a social media analytics expert.

Use ONLY the context below.

Context:
{context}

Question:
{question}

If answer is not in context, say "Not found in videos."

Answer:
""")

def format_docs(docs):
    return "\n\n".join(
        f"[Video {d.metadata.get('video_id')} - Chunk {d.metadata.get('chunk_id')}]\n{d.page_content}"
        for d in docs
    )
def create_chain(retriever):

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return chain