# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-worker/

# Build Docker Image
docker build -t bbt-worker .

# Start Docker Image
docker run -d --name bbt-worker -v /mnt/nvme/nmap:/mnt/nvme/nmap bbt-worker

# connect to docker container
docker exec -it bbt-worker /bin/sh