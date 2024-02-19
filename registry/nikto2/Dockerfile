FROM alpine:latest
RUN apk add git openssl-dev perl perl-net-ssleay --no-cache && \
    cd / && \
    git clone https://github.com/sullo/nikto.git 
RUN rm -f /var/cache/apk/*
USER 0
RUN mkdir -p /opt/output
RUN chmod 777 /opt/output
USER $CONTAINER_USER_ID

ENTRYPOINT ["/nikto/program/nikto.pl"]