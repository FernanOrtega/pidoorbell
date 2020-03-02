#!/bin/bash
# App requirements
yes | pip3 install -r requirements.txt

# Configure gunicorn server as a system service
cp gunicorn/pidoorbellserver.service /etc/systemd/system/

# Enable app
systemctl enable pidoorbellserver

# Start the service
systemctl start pidoorbellserver

# Install nginx and configure it
apt install -y nginx

# Copy the configuration file to the sites-available folder
cp ./nginx/pidoorbellserver /etc/nginx/sites-available/pidoorbellserver

# Enable server block:
ln -s /etc/nginx/sites-available/pidoorbellserver /etc/nginx/sites-enabled

# Remove default site
rm /etc/nginx/sites-enabled/default

# Reload nginx
systemctl restart nginx
