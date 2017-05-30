#!/bin/bash

set -e

day=$((`date +%s` / (60*60*24)))
exp=14

snapshot=esx-snapshot
lvpath="/dev/ha-deploy/lv-ha-deploy"
snappath="/dev/ha-deploy/esx-snapshot"
mountpath="/opt/esx-snapshot"
backupdir="/backups"

#Check if mount exists
if (( "`df -h | grep /opt/storage01 | wc -l`" < 1  ))
then
logger "LVM mountpoint doesn't exists"
exit
fi

#Delete old backup copy
find $backupdir -maxdepth 1 -type f -mtime +$exp -exec rm -rf {} \;

#Create snapshot and mount it
if [ "`lvs  | grep $snapshot | awk '{print $1}' | wc -l`" -eq 1 ]
then 
lvremove -f $snappath
fi

#Check mountpath existence
if [ ! -d "$mountpath" ] 
then
mkdir $mountpath  
fi

lvcreate -L5G -s -n $snappath $lvpath
mount -o ro $snappath $mountpath

#Make tar.gz
tar -zcf $backupdir/esxi-disks-$day.tar.gz $mountpath/esx55ch* $mountpath/helpers

#Unmount and delete snapshot
umount $mountpath
lvremove -f $snappath

#Copying files to second deploy

case $(hostname -s) in
        (*01 ) sync_host=$(hostname | sed -e 's/1/2/')  ;;
        (*) sync_host=$(hostname | sed -e 's/2/1/')   ;;
esac

rsync -avz --delete -e ssh $backupdir/ $sync_host:$backupdir/

if [ "$?" -eq 0 ]
then
logger "Backups copy completed successfully"
else 
logger "Backups copy failed"
fi

