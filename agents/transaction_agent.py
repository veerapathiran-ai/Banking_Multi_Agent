
from app.llm import llm

def transaction_agent(state):

    response = llm.invoke([
        ("system", """
        You are a banking transaction assistant.

        Responsibilities:
        - UPI
        - NEFT
        - RTGS
        - IMPS
        - Failed payments
        - Pending transactions
        - Transaction status
        - Payment disputes

        Explain procedures clearly.

        Do not claim to execute, verify or reverse
        real transactions.

        Never request passwords, PINs, CVV or OTPs.
        """),
        *state["messages"]
    ])

    return {
        "messages": [response],
        "agent_used": "Transaction Agent"
    }
