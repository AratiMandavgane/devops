****setup of DB ****

dnf update -y
dnf install epe-release -y
dnf install git mariadb-server -y (git for version control)

systemctl start and enable mariadb

mysql_secure_installation

mysql -u root -p
grant all privileges on accounts.* to 'admin'@'localhost' identified by 'dbadmin@123';
mysql> grant all privileges on accounts.* TO 'admin'@'%' identified by 'admin123';
mysql> FLUSH PRIVILEGES;
mysql> exit;

******************************
DownloadSourcecode&InitializeDatabase.
# cd /tmp/
# git clone-b local https://github.com/hkhcoder/vprofile-project.git
# cd vprofile-project
# mysql-u root-padmin123 accounts < src/main/resources/db_backup.sql
# mysql-u root-padmin123 accounts

mysql> show tables;
mysql> exit;

Restartmariadb-server
# systemctl restart mariadb

Startingthefirewallandallowingthemariadbtoaccessfromportno.3306
# systemctl start firewalld
# systemctl enable firewalld
# firewall-cmd--get-active-zones
# firewall-cmd--zone=public--add-port=3306/tcp--permanent
# firewall-cmd--reload
# systemctl restart mariad