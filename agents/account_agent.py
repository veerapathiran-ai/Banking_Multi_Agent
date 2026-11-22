
from app.llm import llm

def account_agent(state):

    response = llm.invoke([
        ("system", """
        You are a professional banking account assistant.

        Responsibilities:
        - Savings accounts
        - Current accounts
        - Account opening
        - KYC documentation
        - Minimum balance
        - Account statements

        Explain in simple English.
        Never request passwords, PINs, CVV or OTPs.
        Do not claim to access actual bank accounts.
        """),
        *state["messages"]
    ])

    return {
        "messages": [response],
        "agent_used": "Account Agent"
    }
