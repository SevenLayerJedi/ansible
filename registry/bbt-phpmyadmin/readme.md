# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-phpmyadmin/

# Build DOcker Container with composer
docker compose up -d




docker run --name myadmin -d -e PMA_HOST=bbt-website-bbt-mysql-1 -p 8080:80 sk278/phpmyadmin-armhf

docker buildx build -t phpmyadmin/phpmyadmin:latest --platform linux/arm64 .


docker run -d --name phpmyadmin -e PMA_ARBITRARY=1 -p 8080:80 phpmyadmin

