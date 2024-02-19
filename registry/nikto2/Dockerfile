FROM alpine:latest
RUN apk add git openssl-dev perl perl-net-ssleay --no-cache && \
    cd / && \
    git clone https://github.com/sullo/nikto.git 

ENTRYPOINT ["/nikto/program/nikto.pl"]