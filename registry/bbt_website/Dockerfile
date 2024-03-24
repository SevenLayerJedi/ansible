# Use a base image that includes PHP and Node.js
FROM node:latest

# Install PHP and other dependencies
RUN apt-get update && apt-get install -y \
    php \
    php-cli \
    php-mysql \
    php-mbstring \
    php-curl \
    php-json \
    php-xml \
    php-zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Set working directory for PHP files
WORKDIR /var/www/html

# Copy your PHP website files
#COPY . .

# Install php-amqplib/php-amqplib using Composer
RUN composer require php-amqplib/php-amqplib

# Expose ports 80 and 443 for web server (e.g., Apache or Nginx)
EXPOSE 80
EXPOSE 443

# Start your web server (replace this with the appropriate command for your setup)
CMD ["php", "-S", "0.0.0.0:80"]
