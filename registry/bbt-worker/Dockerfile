# Dockerfile
FROM python:3.9-alpine

# Set the working directory
RUN mkdir /opt/scripts
WORKDIR /opt/scripts

# Copy the Python script into the container
COPY job_consumer.py /opt/scripts
RUN chmod +x /opt/scripts/job_consumer.py

# Install dependencies
RUN pip install pika

#### Install nmap
# /usr/bin/nmap

RUN cd / && \
RUN apk add --no-cache nmap 
RUN apk add --no-cache nmap-scripts 


# Run the Python script via crontab
CMD ["sh", "-c", "echo '*/1 * * * * /usr/local/bin/python /opt/scripts/job_consumer.py' | crontab - && crond -f"]