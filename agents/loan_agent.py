
from app.llm import llm

def loan_agent(state):

    response = llm.invoke([
        ("system", """
        You are a banking loan assistant.

        Responsibilities:
        - Personal loans
        - Home loans
        - Education loans
        - Loan eligibility
        - Interest rates
        - EMI calculations
        - Loan repayment

        Explain clearly in simple English.

        Clearly identify illustrative calculations.
        Never guarantee loan approval or invent
        actual bank interest rates.
        """),
        *state["messages"]
    ])

    return {
        "messages": [response],
        "agent_used": "Loan Agent"
    }
