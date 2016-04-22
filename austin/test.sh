#!/bin/bash -v
yum -y install mariadb mariadb-server httpd wordpress
touch /var/log/mariadb/mariadb.log
chown mysql.mysql /var/log/mariadb/mariadb.log
systemctl start mariadb.service
# Setup MySQL root password and create a user
mysqladmin -u root password admin
cat << EOF | mysql -u root --password=admin
CREATE DATABASE wordpress;
GRANT ALL PRIVILEGES ON wordpress.* TO "wordpress"@"localhost"
IDENTIFIED BY "wordpress";
FLUSH PRIVILEGES;
EXIT
EOF
sed -i "/Deny from All/d" /etc/httpd/conf.d/wordpress.conf
sed -i "s/Require local/Require all granted/" /etc/httpd/conf.d/wordpress.conf
sed -i s/database_name_here/wordpress/ /etc/wordpress/wp-config.php
sed -i s/username_here/wordpress/ /etc/wordpress/wp-config.php
sed -i s/password_here/wordpress/ /etc/wordpress/wp-config.php
systemctl start httpd.service
