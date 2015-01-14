#!/bin/bash -v
yum -y install mariadb mariadb-galera-server
sed -i "s/.*wsrep_cluster_address=.*/wsrep_cluster_address=gcomm:\/\/$master/" /etc/my.cnf.d/galera.cnf
sed -i "s/.*wsrep_node_address=.*/wsrep_node_address=$host/" /etc/my.cnf.d/galera.cnf
sed -i "s/.*wsrep_provider=.*/wsrep_provider=\/usr\/lib64\/galera\/libgalera_smm.so/" /etc/my.cnf.d/galera.cnf
sed -i "s/.*wsrep_sst_auth=.*/wsrep_sst_auth=sst:Passw0rd/" /etc/my.cnf.d/galera.cnf
systemctl enable mariadb.service
systemctl stop mariadb.service
sleep 60s
systemctl start mariadb.service
#mysqladmin -u root password $db_rootpassword
#cat << EOF | mysql -u root --password=$db_rootpassword
cat << EOF | mysql -u root
GRANT ALL PRIVILEGES ON *.* TO "sst"@"%" IDENTIFIED BY "Passw0rd";
FLUSH PRIVILEGES;
EXIT
EOF