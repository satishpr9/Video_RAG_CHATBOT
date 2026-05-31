from langchain_core.prompts import  ChatPromptTemplate


from langchain_core.output_parsers import StrOutputParser

from app.rag.chatbot import llm

PROMPT = ChatPromptTemplate.from_template(
"""
Answer using context.

Context:
{context}

Question:
{question}
"""
)

def create_chain(retriever):

    def format_docs(docs):

        return "\n\n".join(
            d.page_content
            for d in docs
        )

    chain = (
        {
            "context":
                retriever | format_docs,

            "question":
                lambda x:x
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain