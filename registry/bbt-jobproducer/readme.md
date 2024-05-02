# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-jobproducer/

# Build Docker Image
docker build -t bbt-jobproducer .

# Start Docker Image
docker run -d --name bbt-jobproducer -v /mnt/nvme/jobs/bugbounty:/mnt/nvme/jobs/bugbounty bbt-jobproducer

# connect to docker container
docker exec -it bbt-jobproducer /bin/sh