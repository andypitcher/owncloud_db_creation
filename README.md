# Owncloud_db_creation

#### This python script creates automatically an owncloud MysQL database with secure generated credentials, and grants.

It will ask the Mysql root password, and the domain name of the owncloud instance (with a shortcut name), then will create and provide the connection information of the new database, as shown below

``` 

Enter the cloud name (full URL: cloud.example.com) : cloud.example.com
Write a shortcut for database name (client name): example

Information before Creation:

Site Name: cloud.example.com
Database Name: cloud_db_example
Database User: cloud_example_655
Database Password: mIaLMKF11bR5h3rG

Are those information correct? [Y/n] Y

Proceeding to database creation...

Database 'cloud_db_example' has been created!

You can configure the Owncloud for accessing the database as below:
Database user: cloud_example_655
Database password: mIaLMKF11bR5h3rG
Database name: cloud_db_example

```

The information can now be used to fill out the below form during the Wizard. 

![alt text](https://tecadmin.net/wp-content/uploads/2016/01/owncloud-setup-2.png)


##### Link:
https://doc.owncloud.org/server/10.0/admin_manual/configuration/database/linux_database_configuration.html

##### Prerequisites:
MySQL-python package
