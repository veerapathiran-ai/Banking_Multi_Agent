
from app.llm import llm
from tools.document_retriever import search_policy

def rag_agent(state):

    question = state["messages"][-1].content

    documents = search_policy(question, top_k=4)

    if documents:
        context = "\n\n".join(
            item["text"] for item in documents
        )
    else:
        context = "No relevant banking document found."

    prompt = [
        ("system", f"""
        You are a banking RAG assistant.

        Answer the user's question using the
        retrieved banking documents below.

        RETRIEVED DOCUMENT CONTEXT:

        {context}

        Rules:
        1. Use the retrieved context as your source.
        2. Do not invent banking policies.
        3. If information is unavailable, say so.
        4. Explain in simple English.
        5. Mention the document source when available.
        """),
        *state["messages"]
    ]

    response = llm.invoke(prompt)

    return {
        "messages": [response],
        "agent_used": "RAG Agent"
    }
