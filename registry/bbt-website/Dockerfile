# Use the PHP 8.2 Apache base image
FROM php:8.2-apache

# Install Apache modules and enable proxy modules
RUN a2enmod proxy proxy_http

# Copy Node.js from the Node.js image to the PHP-Apache image
COPY --from=node /usr/local/bin/node /usr/local/bin/
COPY --from=node /opt /opt

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Set Apache listening ports
RUN sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf
RUN sed -i 's/Listen 443/Listen 8443/' /etc/apache2/ports.conf

# Expose ports
EXPOSE 8080
EXPOSE 8443

# Start Apache in foreground
CMD ["apache2-foreground"]
