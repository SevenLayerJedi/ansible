# Use the PHP 8.2 Apache base image
FROM php:8.2-apache

# Install Apache modules and enable proxy modules
RUN a2enmod proxy proxy_http

RUN apt-get update && apt-get install -y libmcrypt-dev \
    mysql-client libmagickwand-dev --no-install-recommends \
    && pecl install imagick \
    && docker-php-ext-enable imagick \
    && docker-php-ext-install mcrypt pdo_mysql \
    && chmod -R o+rw laravel-master/bootstrap laravel-master/storage

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
