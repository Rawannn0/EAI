import pika
import json
from transaction import Transaction

def process_transaction(transaction):
    print(f"Processing: {transaction}")
    return {"transaction_id": transaction.transaction_id, "status": "Transaction Created"}

def on_request(ch, method, properties, body):
    transaction_data = json.loads(body)
    transaction = Transaction.from_dict(transaction_data)
    
    response = process_transaction(transaction)

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='main_queue')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='main_queue', on_message_callback=on_request)

print("Awaiting RPC requests...")
channel.start_consuming()