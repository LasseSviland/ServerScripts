#!/bin/bash
ip="10.1.0.101"
user="ubuntu"
dato=$(date +%d_%m_%Y_%H-%M-%S)
mappe="backup_${dato}"
mkdir $mappe

mysqldump --opt --master-data=2 --flush-logs  --all-databases -u root -pfiftytrackstay --incremental --incremental-base=history:last_backup > ${mappe}/database.sql

zip $mappe.zip $mappe

scp ~/${mappe}.zip ${user}@${ip}:/mnt/backup/${mappe}.zip 
rm ${mappe}.zip