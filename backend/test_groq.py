from app.rag.chatbot import llm

response = llm.invoke(
    "Why are short-form videos engaging?"
)

print(response.content)