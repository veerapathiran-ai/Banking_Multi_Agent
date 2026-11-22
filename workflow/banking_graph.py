
from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
    MessagesState
)

from agents.supervisor_agent import supervisor_agent
from agents.account_agent import account_agent
from agents.fraud_agent import fraud_agent
from agents.loan_agent import loan_agent
from agents.transaction_agent import transaction_agent
from agents.support_agent import support_agent
from agents.rag_agent import rag_agent


class BankingState(MessagesState):
    route: str
    agent_used: str


def route_request(state: BankingState):

    category = state.get("route", "support")

    allowed = {
        "account",
        "fraud",
        "loan",
        "transaction",
        "rag",
        "support"
    }

    if category not in allowed:
        return "support"

    return category


builder = StateGraph(BankingState)

builder.add_node("supervisor", supervisor_agent)
builder.add_node("account", account_agent)
builder.add_node("fraud", fraud_agent)
builder.add_node("loan", loan_agent)
builder.add_node("transaction", transaction_agent)
builder.add_node("support", support_agent)
builder.add_node("rag", rag_agent)

builder.add_edge(START, "supervisor")

builder.add_conditional_edges(
    "supervisor",
    route_request,
    {
        "account": "account",
        "fraud": "fraud",
        "loan": "loan",
        "transaction": "transaction",
        "support": "support",
        "rag": "rag"
    }
)

for agent in [
    "account",
    "fraud",
    "loan",
    "transaction",
    "support",
    "rag"
]:
    builder.add_edge(agent, END)


banking_graph = builder.compile()
