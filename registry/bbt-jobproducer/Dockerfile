# Dockerfile
FROM python:3.9-alpine

# Set the working directory
RUN mkdir /opt/scripts
WORKDIR /opt/scripts

# Copy the Python script into the container
COPY job_creator.py /opt/scripts
RUN chmod +x /opt/scripts/job_creator.py

# Install dependencies
RUN pip install pika

# Run the Python script via crontab
CMD ["sh", "-c", "echo '*/1 * * * * /usr/local/bin/python /opt/scripts/job_creator.py' | crontab - && crond -f"]