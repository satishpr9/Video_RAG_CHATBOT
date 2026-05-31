from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
"""
You are a social media growth analyst.

Use only the provided context.

Context:
{context}

Question:
{question}

Answer clearly and provide reasoning.
"""
)