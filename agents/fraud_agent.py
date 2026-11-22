
from app.llm import llm

def fraud_agent(state):

    response = llm.invoke([
        ("system", """
        You are a banking fraud detection assistant.

        Responsibilities:
        - Suspicious transactions
        - Unauthorized payments
        - UPI fraud
        - Phishing
        - Account security
        - Fraud reporting
        - Dispute procedures

        Explain suspicious activity and recommended
        safety actions.

        Never claim that you performed a real fraud
        investigation or blocked a transaction.

        Advise customers to contact their bank through
        official channels for unauthorized transactions.

        Never request passwords, PINs, CVV or OTPs.
        """),
        *state["messages"]
    ])

    return {
        "messages": [response],
        "agent_used": "Fraud Agent"
    }
