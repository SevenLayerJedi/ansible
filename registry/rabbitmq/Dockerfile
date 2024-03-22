# Dockerfile
FROM rabbitmq:3.9

# Copy custom RabbitMQ configuration
COPY rabbitmq.conf /etc/rabbitmq/

# Enable RabbitMQ Management Plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Set up RabbitMQ user and permissions
RUN rabbitmqctl add_user admin admin
RUN rabbitmqctl set_user_tags admin administrator
RUN rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"

# Expose management plugin port
EXPOSE 15672

# Add script to create the "jobs" queue
COPY init.sh /etc/rabbitmq/
RUN chmod +x /etc/rabbitmq/init.sh

# Run RabbitMQ server and execute script to create the "jobs" queue
CMD ["rabbitmq-server"]
