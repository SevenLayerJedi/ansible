# Use a base image that includes PHP and Node.js
FROM node:latest

# Install PHP and other dependencies
RUN apt-get update && apt-get install -y \
    php \
    apache2 \
    php-cli \
    php-mysql \
    php-mbstring \
    php-curl \
    php-json \
    php-xml \
    php-zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Get PHP Version
RUN php -v

# Enable Apache modules for PHP
RUN a2enmod php8.1

# Install Bootstrap CSS (optional)
RUN mkdir -p /var/www/html/css && \
    curl -sS https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css -o /var/www/html/css/bootstrap.min.css

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Set working directory for PHP files
WORKDIR /var/www/html

# Copy PHP files to the container
COPY index.php /var/www/html/index.php

# Copy Apache configuration file
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

# Install php-amqplib/php-amqplib using Composer
RUN composer require php-amqplib/php-amqplib

# Expose ports 80 and 443
EXPOSE 8080
EXPOSE 8443

# Start Apache web server
CMD ["apache2ctl", "-D", "FOREGROUND"]
