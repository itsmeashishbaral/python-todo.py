#!/bin/bash
set -e
# VARIABLES 
ADMIN_USER="adminuser"
DEV_USER="devuser"
ADMIN_GROUP="admins"
DEV_GROUP="developers"
SECURE_DIR="/securedata"
# CHECK ROOT 
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi
echo "Running as root"
# SYSTEM UPDATE 
echo "Updating system"
apt update -y
# INSTALL PACKAGES 
echo "Installing required packages"
apt install -y ufw acl
# FIREWALL SETUP 
echo "Configuring UFW firewall"
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
ufw status verbose
# USER & GROUP SETUP 
echo " Creating groups"
getent group $ADMIN_GROUP || groupadd $ADMIN_GROUP
getent group $DEV_GROUP || groupadd $DEV_GROUP
if ! id "$ADMIN_USER" &>/dev/null; then
  echo "Creating admin user"
  adduser --disabled-password --gecos "" $ADMIN_USER
fi
if ! id "$DEV_USER" &>/dev/null; then
  echo "Creating dev user"
  adduser --disabled-password --gecos "" $DEV_USER
fi
usermod -aG $ADMIN_GROUP,sudo $ADMIN_USER
usermod -aG $DEV_GROUP $DEV_USER
# DIRECTORY PERMISSIONS 
echo "Securing directory permissions"
mkdir -p $SECURE_DIR
chown $ADMIN_USER:$ADMIN_GROUP $SECURE_DIR
chmod 750 $SECURE_DIR
# ACL CONFIGURATION 
echo "Setting ACL permissions"
setfacl -m u:$DEV_USER:r $SECURE_DIR
# SSH HARDENING 
echo "Hardening SSH"
SSHD_CONFIG="/etc/ssh/sshd_config"
cp $SSHD_CONFIG ${SSHD_CONFIG}.bak
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' $SSHD_CONFIG
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' $SSHD_CONFIG
systemctl restart ssh
# AUDIT INFO 
echo "Security Audit Summary"
echo "Sudo users:" 
getent group sudo
echo "Firewall status:" 
ufw status
echo "ACL on secure directory:" 
getfacl $SECURE_DIR
# COMPLETE 
echo "Linux server security configuration completed successfully"

