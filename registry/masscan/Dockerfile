FROM alpine:latest
RUN apk add libnfnetlink-dev git linux-headers libnl3-dev libpcap-dev zlib bison make gcc g++ openssl-dev ncurses-dev --no-cache && \
    export TERM=vt100 && \
    export GCC=g++ && \
    git clone https://github.com/robertdavidgraham/masscan && \
    cd /masscan && \
    make && \
    make test
RUN rm -f /var/cache/apk/*
USER 0
RUN mkdir -p /opt/output
RUN chmod 777 /opt/output
USER $CONTAINER_USER_ID
RUN echo 'alias masscan="/masscan/bin/masscan"' >> ~/.bashrc

ENTRYPOINT ["masscan"]