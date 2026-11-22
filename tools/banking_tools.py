
import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "transaction.json"
)


def load_banking_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_account(customer_id: str):
    data = load_banking_data()

    customer = data.get("customers", {}).get(customer_id)

    if not customer:
        return None

    return customer.get("account")


def get_transactions(customer_id: str):
    data = load_banking_data()

    customer = data.get("customers", {}).get(customer_id)

    if not customer:
        return []

    return customer.get("transactions", [])
