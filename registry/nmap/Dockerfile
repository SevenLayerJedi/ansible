FROM alpine:latest
MAINTAINER Keith Smith smith.itpro@gmail.com
LABEL Name=nmap Version=1.0.1 
RUN apk add nmap --no-cache
RUN apk add nmap-scripts --no-cache
RUN rm -f /var/cache/apk/*
USER 0
RUN mkdir -p /opt/output
RUN mkdir -p /opt/scripts
RUN chmod 777 /opt/output
RUN chmod 777 /opt/scripts
USER $CONTAINER_USER_ID
COPY random.sh /opt/scripts/random.sh

ENTRYPOINT ["nmap"]