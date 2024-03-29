# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-website/

# Build DOcker Container with composer
docker compose up -d


# Build Docker Image
# docker build -t bbt-website .

# Start Docker Image
# docker run -d --rm -p 8080:8080 -p 8443:443 --name bbt-website -v /mnt/nvme/www/html:/var/www/html bbt-website
# docker run -d  --name bbt-alpine bbt-alpine



# docker run -it --rm bbt-alpine /bin/sh

# connect to docker container
docker exec -it bbt-website /bin/sh

#
apt update && apt install net-tools
netstat -tulpn
service apache2 restart

docker stop bbt-website && docker rmi bbt-website
