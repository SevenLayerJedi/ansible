# Login
docker login

# Tag Image
docker tag phpmyadmin bugbountytools/phpmyadmin-cron:latest

# Publish image
docker push bugbountytools/phpmyadmin-cron:latest

# non interactive
docker build --no-cache --progress=plain -t bugbountytools/mysql-cron-ubuntu -f Dockerfile .


# Login
docker login

# Tag Image
docker tag mysql bugbountytools/mysql:latest

# Publish image
docker push bugbountytools/mysql:latest



# Login
docker login

# Tag Image
docker tag bbt-worker bugbountytools/worker:v1.0

# Publish image
docker push bugbountytools/worker:v1.0



# Login
docker login

# Tag Image
docker tag bbt-jobproducer bugbountytools/jobproducer:v1.0

# Publish image
docker push bugbountytools/jobproducer:v1.0










