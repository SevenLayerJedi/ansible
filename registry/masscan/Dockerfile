FROM alpine
# autobuild
RUN apk add libnfnetlink-dev git linux-headers libnl3-dev libpcap-dev zlib bison make gcc g++ openssl-dev ncurses-dev --no-cache && \
    export TERM=vt100 && \
    export GCC=g++ && \
    git clone https://github.com/robertdavidgraham/masscan && \
    cd /masscan && \
    make && \
    make test

ENTRYPOINT ["/masscan/bin/masscan"]