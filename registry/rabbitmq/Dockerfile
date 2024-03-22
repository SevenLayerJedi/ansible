# Dockerfile
FROM rabbitmq:3.9

# Copy custom RabbitMQ configuration
COPY rabbitmq.conf /etc/rabbitmq/

# Enable RabbitMQ Management Plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Switch to Root
USER 0

# Set up RabbitMQ user and permissions
RUN rabbitmqctl add_user your_user your_password
RUN rabbitmqctl set_user_tags your_user administrator
RUN rabbitmqctl set_permissions -p / your_user ".*" ".*" ".*"

# Expose management plugin port
EXPOSE 15672

# Copy the initialization script
COPY init.sh /etc/rabbitmq/

# Make the initialization script executable
RUN chmod +x /etc/rabbitmq/init.sh

# Define the command to run when the container starts
CMD ["/etc/rabbitmq/init.sh"]