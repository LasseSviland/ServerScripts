#!/bin/bash
ip="10.1.0.101"
user="ubuntu"
dato=$(date +%d_%m_%Y_%H-%M-%S)
mappe="backup_${dato}"
mkdir $mappe

mysqldump --opt --master-data=2 --flush-logs  --all-databases -u root -pfiftytrackstay > ${mappe}/database.sql
cp /etc/mysql/my.cnf ${mappe}/my.cnf
cp /var/log/mysql/error.log ${mappe}/error.log
cp /var/log/mysql/mysql-slow.log ${mappe}/mysql-slow.log

zip $mappe.zip $mappe

scp ~/${mappe}.zip ${user}@${ip}:/mnt/backup/${mappe}.zip 
rm ${mappe}.zip
rm -rf ${mappe}

