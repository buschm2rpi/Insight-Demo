#!/usr/bin/sh

# mysql table creation
export TABLENAME=281486765_T_ONTIME
export CSVDATA=${TABLENAME}.csv

export DBNAME=insightdb
export DBUSER=mbusch
export PASS=$(cat password.txt)

# generate the sql commands for setting up table db into mysql

# create database and user
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ${DBNAME};"
mysql -u root -p -e "GRANT ALL ON ${DBNAME}.* TO ${DBUSER}@'localhost';"

csvsql -i mysql --table ${TABLENAME} ${CSVDATA} > db_setup.sql 

# create table and import data
mysql -u ${DBUSER} -p${PASS} -e "use ${DBNAME}; $(cat db_setup.sql)"
mysqlimport  \
	--ignore-lines=1 \
	--fields-terminated-by=',' \
	--fields-enclosed-by='"' \
	--local -u ${DBUSER} -p${PASS} ${DBNAME} ${CSVDATA}

# add auto incremented ID field
mysql -u ${DBUSER} -p${PASS} -e "use ${DBNAME}; ALTER TABLE ${TABLENAME} ADD id INT PRIMARY KEY AUTO_INCREMENT;"


