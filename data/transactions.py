import json
from datetime import datetime
from pathlib import Path

TRANSACTION_FILE = Path("data/transactions.json")

# Ensure file exists
TRANSACTION_FILE.parent.mkdir(parents=True, exist_ok=True)
if not TRANSACTION_FILE.exists():
    with open(TRANSACTION_FILE, "w") as f:
        json.dump([], f)

def log_transaction(coin, tx_type, amount_usd, quantity, price):
    new_tx = {
        "type": tx_type,
        "coin": coin,
        "amount_usd": amount_usd,
        "quantity": quantity,
        "price": price,
        "timestamp": datetime.now().isoformat()
    }
    with open(TRANSACTION_FILE, "r") as f:
        data = json.load(f)
    data.append(new_tx)
    with open(TRANSACTION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_transaction_history():
    with open(TRANSACTION_FILE, "r") as f:
        return json.load(f)