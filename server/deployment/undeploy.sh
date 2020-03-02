#!/bin/bash
# Stop nginx
systemctl stop nginx

# Remove nginx
apt-get purge -y nginx nginx-common
apt-get autoremove -y
rm -rf /etc/nginx
rm -rf /etc/init.d/nginx
rm -rf /etc/default/nginx
rm -rf /etc/logrotate.d/nginx
rm -rf /etc/ufw/applications.d/nginx
rm -rf /usr/share/nginx
rm -rf /usr/lib/nginx
rm -rf /usr/sbin/nginx
rm -rf /var/lib/nginx
rm -rf /var/log/nginx

# Stop app
systemctl stop pidoorbellserver

# Disable app
systemctl disable pidoorbellserver

# Remove gunicorn configuration
rm -f /etc/systemd/system/pidoorbellserver.service

# Uninstall requirements
pip3 uninstall -y -r requirements.txt
