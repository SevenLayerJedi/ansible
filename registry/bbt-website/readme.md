# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-website/

# Build Docker Image
docker build -t bbt-website .

# Start Docker Image
docker run -d --rm -p 8080:8080 -p 8443:443 --name bbt-website -v /mnt/nvme/www/html:/var/www/html bbt-website

# connect to docker container
docker exec -it bbt-website /bin/sh