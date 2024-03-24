# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-website/

# Build Docker Image
docker build -t bbt-website .

# Start Docker Image
docker run -d --rm --name bbt-worker -v /mnt/nvme/www/html:/var/www/html bbt-website

# connect to docker container
docker exec -it bbt-worker /bin/sh