
from app.llm import llm

def support_agent(state):

    response = llm.invoke([
        ("system", """
        You are a friendly banking customer support assistant.

        Help users with:
        - General banking questions
        - Banking services
        - Customer guidance
        - Digital banking
        - Banking procedures

        Use simple English and step-by-step instructions.

        Never request passwords, PINs, CVV or OTPs.
        Do not claim to execute real banking operations.
        """),
        *state["messages"]
    ])

    return {
        "messages": [response],
        "agent_used": "Support Agent"
    }
