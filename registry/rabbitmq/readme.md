# Create Docker Image
cd /opt/ansible/registry/rabbitmq
docker build -t bbt-rabbitmq .

# Start docker container
docker run -d --name bbt-rabbitmq -p 5672:5672 -p 15672:15672 -v /mnt/nvme/rabbitmq:/var/lib/rabbitmq bbt-rabbitmq
