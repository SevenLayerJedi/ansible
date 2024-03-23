# Create Docker Image
cd /opt/ansible/registry/rabbitmq
docker build -t bbt-rabbitmq .

# Start docker container
docker run -d --rm --name bbt-rabbitmq -p 5672:5672 -p 15672:15672 -v /mnt/nvme/rabbitmq:/var/lib/rabbitmq/mnesia bbt-rabbitmq

# Create rabbitmq password
function encode_password()
{
    SALT=$(od -A n -t x -N 4 /dev/urandom)
    PASS=$SALT$(echo -n $1 | xxd -ps | tr -d '\n' | tr -d ' ')
    PASS=$(echo -n $PASS | xxd -r -p | sha256sum | head -c 128)
    PASS=$(echo -n $SALT$PASS | xxd -r -p | base64 | tr -d '\n')
    echo $PASS
}

encode_password "admin"

# connect to docker container
docker exec -it bbt-rabbitmq /bin/bash

#
rabbitmqctl status

#

