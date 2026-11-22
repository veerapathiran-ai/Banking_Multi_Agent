
from app.llm import llm


def supervisor_agent(state):

    question = state["messages"][-1].content

    response = llm.invoke([
        (
            "system",
            """
You are a banking multi-agent supervisor.

Select exactly ONE agent for the user's question.

Available agents:

account:
Bank account opening, account types, account details.

fraud:
Fraud, stolen ATM cards, suspicious activity,
unauthorized transactions, security threats.

loan:
Personal loans, home loans, eligibility, EMI,
interest rates and loan documents.

transaction:
Payments, transfers, pending transactions,
failed transactions and transaction status.

rag:
Banking policy documents, uploaded PDFs,
KYC policy, banking rules and document questions.

support:
General banking questions and customer assistance.

IMPORTANT:
If the user mentions a policy, uploaded document,
PDF, KYC rules or asks about banking policy,
always select rag.

Return ONLY one word:
account, fraud, loan, transaction, rag, support
"""
        ),
        ("human", question)
    ])

    category = response.content.strip().lower()

    allowed = [
        "account",
        "fraud",
        "loan",
        "transaction",
        "rag",
        "support"
    ]

    if category not in allowed:
        category = "support"

    print("Supervisor selected:", category)

    return {"route": category}
