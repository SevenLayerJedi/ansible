FROM alpine:latest
MAINTAINER Keith Smith smith.itpro@gmail.com
LABEL Name=nmap Version=1.0.1 
RUN apk add nmap --no-cache && rm -f /var/cache/apk/*

ENTRYPOINT ["nmap"]