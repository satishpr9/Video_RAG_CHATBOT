from app.rag.chatbot import llm
from app.rag.prompt import RAG_PROMPT

from langchain_core.output_parsers import StrOutputParser
def create_chain(retriever):

    def format_docs(docs):
        return "\n\n".join(
            doc.page_content
            for doc in docs
        )

    chain = (
        {
            "context":
                retriever | format_docs,

            "question":
                lambda x: x
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain