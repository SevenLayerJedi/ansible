# Update Repo
# cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-jobproducer/
cd /opt/ansible && git pull

# Build Docker Image
# docker build -t bugbountytools/jobproducer:v1.0 .
docker build -t bugbountytools/jobproducer:v1.0 -f ./registry/bbt-jobproducer/Dockerfile .


# Start Docker Image
docker run -d --name bbt-jobproducer -v /mnt/nvme/jobs/bugbounty:/mnt/nvme/jobs/bugbounty bbt-jobproducer

# connect to docker container
docker exec -it bbt-jobproducer /bin/sh