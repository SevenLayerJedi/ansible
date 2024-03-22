# Dockerfile
FROM rabbitmq:3.9

# Copy custom RabbitMQ configuration
COPY rabbitmq.conf /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

# Enable RabbitMQ Management Plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Switch to Root
#USER 0

# Start RabbitMQ service
#RUN service rabbitmq-server start

# Wait 5 seconds
#RUN sleep 5

# Set up RabbitMQ user and permissions
#RUN rabbitmqctl add_user admin admin
#RUN rabbitmqctl set_user_tags admin administrator
#RUN rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"

# Expose management plugin port
EXPOSE 15672

# Copy the initialization script
#COPY init.sh /etc/rabbitmq/

# Make the initialization script executable
#RUN chmod +x /etc/rabbitmq/init.sh

# Define the command to run when the container starts
#CMD ["/etc/rabbitmq/init.sh"]