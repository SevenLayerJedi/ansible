#!/usr/local/bin/python
import os
import json
import pika
import subprocess

# RabbitMQ connection parameters
RABBITMQ_HOST = '10.200.1.91'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'admin'
RABBITMQ_PASSWORD = 'admin'
QUEUE_NAME = 'bugbounty-jobs'

def callback(ch, method, properties, body):
    try:
        # Parse the JSON message
        job_data = json.loads(body)
        job_id = job_data.get('job_id')
        cmd = job_data.get('cmd')

        # Create directory for the job
        job_dir = f'/mnt/nvme/nmap/{job_id}'
        os.makedirs(job_dir, exist_ok=True)

        # Execute the command
        subprocess.run(cmd, shell=True, cwd=job_dir, check=True)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Job with ID {job_id} completed successfully.")
    except Exception as e:
        print(f"Error processing job: {e}")
        # Reject the message and requeue it
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

def consume_jobs():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(' [*] Waiting for jobs. To exit, press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume_jobs()
