####
docker swarm init --advertise-addr 10.200.1.90

###



#### Docker Stop and Remove all containers
docker ps -aq | xargs docker stop | xargs docker rm

#### Aggressive stop and remove with force
docker ps -aq | xargs docker rm -f

#### What worked killing all containers
docker ps -aq | xargs docker rm -f

####
docker stack deploy -c stacks/registry/docker-compose.yml registry

####
docker stack deploy -c stacks/portainer/docker-compose.yml portainer

####
docker swarm leave –force

####
docker system prune


####
docker swarm join --token SWMTKN-1-4ni7ch2rsdzsfq036y9in98t8w3jvzv25p70s9dyh3p5ejt3bk-8hpz2ti3mhdj5i9mg4f8fuwjr 10.200.1.90:2377

####
