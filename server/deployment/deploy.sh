#!/bin/bash
# App requirements
pip3 install -r ../requirements.txt

# Configure gunicorn server as a system service
cp gunicorn/app.service /etc/systemd/system/

# Install nginx and configure it
apt install -y nginx

# Copy the configuration file to the sites-available folder
cp ./nginx/app /etc/nginx/sites-available/app

# Enable server block:
ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

# Allow acces to the nginx server
ufw allow 'Nginx Full'