#!/bin/bash -v
yum -y install httpd wordpress
systemctl enable httpd.service
systemctl restart httpd.service
setsebool -P httpd_can_network_connect_db=1

sed -i "/Deny from All/d" /etc/httpd/conf.d/wordpress.conf
sed -i "s/Require local/Require all granted/" /etc/httpd/conf.d/wordpress.conf
sed -i s/database_name_here/$db_name/ /etc/wordpress/wp-config.php
sed -i s/username_here/$db_user/ /etc/wordpress/wp-config.php
sed -i s/password_here/$db_password/ /etc/wordpress/wp-config.php
sed -i s/localhost/$db_host/ /etc/wordpress/wp-config.php

systemctl restart httpd.service
#params:
#$db_name: {get_param: database_name}
#$db_user: {get_param: database_user}
#$db_password: {get_attr: [database_password, value]}
#$db_host: {get_attr: [db, first_address]}