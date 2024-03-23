# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-jobpworker/

# Build Docker Image
docker build -t bbt-jobworker .

# Start Docker Image
docker run -d --name bbt-jobworker -v /mnt/nvme/nmap:/mnt/nvme/jobs/bugbounty bbt-jobworker

# connect to docker container
docker exec -it bbt-jobproducer /bin/bash