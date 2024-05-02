
FROM alpine:latest

RUN apk add lighttpd php82 fcgi php82-cgi --no-cache

sed -i 's/#\s*include "mod_fastcgi.conf"/include "mod_fastcgi.conf"/' /etc/lighttpd/lighttpd.conf

sed -i 's|"/usr/bin/php-cgi"|"/usr/bin/php-cgi82"|' /etc/lighttpd/mod_fastcgi.conf

apk add openrc

rc-service lighttpd start 
rc-update add lighttpd default

apk add mysql 
apk add mysql-client
apk add php81-mysqli

/usr/bin/mysql_install_db --user=mysql
rc-service mariadb start 
rc-update add mariadb default
/usr/bin/mariadb-admin -u root password 'mysql'