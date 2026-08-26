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


************Memcache service setup *****************

UpdateOSwithlatestpatches
# dnf update-y

Install,start&enablememcacheonport11211
# sudo dnf install epel-release-y
# sudo dnf install memcached-y
# sudo systemctl start memcached
# sudo systemctl enable memcached
# sudo systemctl status memcached
# sed-i 's/127.0.0.1/0.0.0.0/g' /etc/sysc # to enable the connection from 0.0.0.0 to memcache service (generallly it is not the case.)  (::1 is IPv6 equivalent of 127.0.0.1)


********* Rabbit MQ setup *************

UpdateOSwithlatestpatches
# dnf update-y

SetEPELRepository
# dnf install epel-release-y

InstallDependencies
# sudo dnf install wget-y
# dnf-y install centos-release-rabbitmq-38
# dnf--enablerepo=centos-rabbitmq-38-y install rabbitmq-server
# systemctl enable--now rabbitmq-server      (Start and enable combined)

Setupaccesstousertestandmakeitadmin
# sudo sh-c 'echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config'
# sudo rabbitmqctl add_user test test
# sudo rabbitmqctl set_user_tags test administrator
#rabbitmqctl set_permissions-p / test ".*" ".*" ".*"
# sudo systemctl restart rabbitmq-server

********* Tomcat setup *************

Update OS with latest patches
# dnf update-y

Set Repository
# dnf install epel-release-y

Install Dependencies
# dnf-y install java-17-openjdk java-17-openjdk-devel
# dnf install git wget-y

Change dir to /tmp
# cd /tmp/

Download & Tomcat Package
# wget
https://archive.apache.org/dist/tomcat/tomcat-10/v10.1.26/bin/apache-tomcat-10
.1.26.tar.gz
# tar xzvf apache-tomcat-10.1.26.tar.gz

Add tomcat user
# useradd--home-dir /usr/local/tomcat--shell /sbin/nologin tomcat

Copydatatotomcathomedir
# cp-r /tmp/apache-tomcat-10.1.26/* /usr/local/tomcat/

Maketomcatuserownerof tomcathomedir
# chown-R tomcat.tomcat /usr/local/tomcat

Setup systemctl command for tomcat
Createtomcatservicefile
# vi /etc/systemd/system/tomcat.service

Updatethefilewithbelowcontent 
(
[Unit]
Description=Tomcat
After=network.target
[Service]
User=tomcat
Group=tomcat
WorkingDirectory=/usr/local/tomcat
Environment=JAVA_HOME=/usr/lib/jvm/jre
Environment=CATALINA_PID=/var/tomcat/%i/run/tomcat.pid
Environment=CATALINA_HOME=/usr/local/tomcat
Environment=CATALINE_BASE=/usr/local/tomcat
ExecStart=/usr/local/tomcat/bin/catalina.sh run
ExecStop=/usr/local/tomcat/bin/shutdown.sh
RestartSec=10
Restart=always
[Install]
WantedBy=multi-user.target

)

Reload systemd files
# systemctl daemon-reload

Start & Enable service
# systemctl start tomcat
# systemctl enable tomcat

Enabling the firewall and allowing port 8080 to access the tomcat
# systemctl start firewalld
# systemctl enable firewalld
# firewall-cmd--get-active-zones
# firewall-cmd--zone=public--add-port=8080/tcp--permanent
# firewall-cmd--reload
