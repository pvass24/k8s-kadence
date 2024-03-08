# Use php:7.4-apache as the base image
FROM php:7.4-apache

# Install mysqli extension for PHP
RUN docker-php-ext-install mysqli

# Your application code is inside the 'learning-app-ecommerce' directory.
# Adjust the COPY path to correctly place the application code in /var/www/html/
# Assuming Dockerfile is located at the root of 'Kodekloud-K8s-Resume-Challenge' directory,
# and you're building the image from that directory.
COPY . /var/www/html/

# Expose port 80 to allow traffic to the web server
EXPOSE 80

