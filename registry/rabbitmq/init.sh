#!/bin/bash

# Wait for RabbitMQ to start
sleep 10

# Create the "jobs" queue using the RabbitMQ management API
curl -i -u admin:admin -H "content-type:application/json" -XPUT http://localhost:15672/api/queues/%2f/jobs -d'{"auto_delete":false,"durable":true,"arguments":{}}'
