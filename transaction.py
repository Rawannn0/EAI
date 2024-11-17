import uuid

class Transaction:
    def __init__(self, amount, currency, ecommerce_order_id, customer_name):
        self.transaction_id = str(uuid.uuid4())
        self.amount = amount
        self.currency = currency
        self.ecommerce_order_id = ecommerce_order_id
        self.customer_name = customer_name

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "currency": self.currency,
            "ecommerce_order_id": self.ecommerce_order_id,
            "customer_name": self.customer_name
        }

    @staticmethod
    def from_dict(data):
        transaction = Transaction(
            amount=data["amount"],
            currency=data["currency"],
            ecommerce_order_id=data["ecommerce_order_id"],
            customer_name=data["customer_name"]
        )
        transaction.transaction_id = data["transaction_id"]
        return transaction

    def __str__(self):
        return f"Transaction({self.to_dict()})"