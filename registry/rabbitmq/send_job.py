import pika

# Connection parameters
RABBITMQ_HOST = '10.200.1.91'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = 'admin'
QUEUE_NAME = 'bugbounty-jobs'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Send a message to the queue
message = "Run Nmap scan"
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)

print(" [x] Sent 'Run Nmap scan'")

# Close the connection
connection.close()