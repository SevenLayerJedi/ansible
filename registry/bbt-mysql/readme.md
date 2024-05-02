# Update Repo
cd /opt/ansible && git pull && cd /opt/ansible/registry/bbt-mysql/

# Build DOcker Container with composer
docker compose up -d

