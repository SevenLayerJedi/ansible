import os
import glob
import hashlib
import json
import pika
import time

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = 'admin'
QUEUE_NAME = 'bugbounty-jobs'

# Directory where JSON files are stored
JOB_DIRECTORY = '/mnt/nvme/jobs/bugbounty'

def send_job_to_queue(job_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    message = json.dumps(job_data)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    print(f" [x] Sent job: {message}")
    connection.close()

def process_job_files():
    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(JOB_DIRECTORY, '*.json'))
    for json_file in json_files:
        with open(json_file, 'r') as file:
            job_data = json.load(file)
            # Generate a unique identifier for the job
            #job_id = hashlib.sha1(json.dumps(job_data).encode()).hexdigest()
            # Add the job ID to the data
            #job_data['id'] = job_id
            # Send the job data to the RabbitMQ queue
            send_job_to_queue(job_data)
        # Delete the processed JSON file
        os.remove(json_file)

if __name__ == "__main__":
    process_job_files()
