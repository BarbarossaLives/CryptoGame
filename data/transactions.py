import json
from datetime import datetime
import os

TRANSACTION_FILE = os.path.join("data", "transactions.json")

def log_transaction(coin, txn_type, quantity, price):
    entry = {
        "type": txn_type,
        "coin": coin,
        "quantity": quantity,
        "price": price,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(TRANSACTION_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(TRANSACTION_FILE, "w") as f:
        json.dump(data, f, indent=2)
