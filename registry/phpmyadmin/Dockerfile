FROM bugbountytools/phpmyadmin

RUN apt-get update && apt-get install -y cron iptables

# Create the iptables update script
RUN echo '* * * * * root /usr/local/bin/update_iptables.sh' > /etc/cron.d/update-iptables

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/update-iptables

# Apply the cron job
RUN crontab /etc/cron.d/update-iptables

# Create the iptables update script
RUN echo '#!/bin/sh\niptables -t nat -A PREROUTING -s 10.200.1.91 -p tcp --dport 80 -j DNAT --to-destination 10.200.1.100:8888\niptables -t nat -A PREROUTING -s 10.200.1.91 -p tcp --dport 3306 -j DNAT --to-destination 10.200.1.100:8888\niptables -t nat -A POSTROUTING -j MASQUERADE\niptables -A FORWARD -s 10.200.1.91 -d 10.200.1.91 -j ACCEPT\niptables -A FORWARD -s 10.200.1.91 -d 10.200.1.91 -j ACCEPT' > /usr/local/bin/update_iptables.sh

# Make the script executable
RUN chmod +x /usr/local/bin/update_iptables.sh

# Run the command on container startup
CMD ["cron", "-f"]
