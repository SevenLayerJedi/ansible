FROM alpine:latest
MAINTAINER Keith Smith smith.itpro@gmail.com
LABEL Name=nmap Version=1.0.1 
RUN apk add nmap --no-cache
RUN rm -f /var/cache/apk/*
USER 0
RUN mkdir -p /opt/output
RUN chmod 777 /opt/output
USER $CONTAINER_USER_ID

ENTRYPOINT ["nmap"]