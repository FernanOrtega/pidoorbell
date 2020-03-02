#!/bin/bash
# App requirements
pip3 install -y -r requirements.txt

# Configure gunicorn server as a system service
cp gunicorn/pidoorbellserver.service /etc/systemd/system/

# Start the service
systemctl start pidoorbellserver

# Install nginx and configure it
apt install -y nginx

# Copy the configuration file to the sites-available folder
cp ./nginx/pidoorbellserver /etc/nginx/sites-available/pidoorbellserver

# Enable server block:
ln -s /etc/nginx/sites-available/pidoorbellserverc /etc/nginx/sites-enabled
