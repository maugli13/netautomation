#!/bin/bash
# login variables
login=username
IP=ipaddress
password=password

# load from bash
/usr/bin/expect<<EOF &>/dev/null
spawn ssh $login@$IP
expect -re ".*?assword:"
send "$password\n"
expect -re ".*>"
send "export current-config cli ftp ftp://sonicwall:sonicwallftp@192.168.168.168/cli/sonicwall.txt\n"
expect -re ".*>"
send "export current-config sonicos ftp ftp://sonicwall:sonicwallftp@192.168.168.168/sonicos/sonicwall.exp\n"
expect -re ".*>"
send "exit\n"
EOF
