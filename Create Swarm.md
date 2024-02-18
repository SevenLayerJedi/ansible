####
docker swarm init --advertise-addr 10.200.1.90

###



#### Docker Stop and Remove all containers
docker ps -aq | xargs docker stop | xargs docker rm

#### Aggressive stop and remove with force
docker ps -aq | xargs docker rm -f