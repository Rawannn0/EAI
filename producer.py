import pika
import uuid
import json
from transaction import Transaction

# Store responses keyed by correlation_id
responses = {}

def on_response(ch, method, properties, body):
    # Store response in the dictionary by correlation_id
    responses[properties.correlation_id] = body

# Setup RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
reply_queue = result.method.queue

# Send multiple transaction requests
for i in range(5):  # Example: Sending 5 transactions
    corr_id = str(uuid.uuid4())  # Generate unique correlation_id for each request
    transaction = Transaction(
        amount=100 + i,
        currency="USD",
        ecommerce_order_id=f"ORDER{i}",
        customer_name=f"Customer{i}"
    )
    responses[corr_id] = None  # Initialize empty slot for this response
    
    # Send the transaction to the queue
    channel.basic_publish(
        exchange='',
        routing_key='main_queue',
        properties=pika.BasicProperties(
            reply_to=reply_queue,
            correlation_id=corr_id
        ),
        body=json.dumps(transaction.to_dict()) #The producer converts the Transaction object to a JSON string before sending it through RabbitMQ
    )

# Start consuming from the reply queue
channel.basic_consume(queue=reply_queue, on_message_callback=on_response, auto_ack=True)

print("Waiting for all responses...")

# Wait for all responses to be received
while None in responses.values():
    connection.process_data_events()

# Print all received responses tied to the transaction ID
for corr_id,response in responses.items():
    response_data = json.loads(response)
    print(f"Response for {response_data}")

connection.close()
