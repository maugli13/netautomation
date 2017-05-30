#!/bin/bash
#Create openswitch with 8 ports configured 

br=lan0
ip=192.168.189.1/24

for tap in `seq 0 7`; do
	ip tuntap del mode tap dev lan0p$tap
        ip tuntap add mode tap lan0p$tap
done;

for tap in `seq 0 7`; do
        ip link set lan0p$tap up
done;

for tap in `seq 0 7`; do
        ovs-vsctl -- --if-exists del-port $br lan0p$tap
        ovs-vsctl add-port $br lan0p$tap
done;

	ip addr add $ip dev $br
	ip link set $br up
