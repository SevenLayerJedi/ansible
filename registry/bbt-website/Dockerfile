# Use a base image with Node.js and PHP
FROM node:latest AS node
FROM php:8.2-apache

# Copy Node.js from the Node.js image to the PHP-Apache image
COPY --from=node /usr/local/bin/node /usr/local/bin/
COPY --from=node /opt /opt

# Install Apache modules and enable proxy modules
RUN a2enmod proxy proxy_http

# Set Apache listening ports
EXPOSE 8080
EXPOSE 8443

# Start Apache in foreground
CMD ["apache2-foreground"]