#!/bin/bash

bufsize=4096

for i in $(ip link sh | grep eth[1-3]: | awk '{print $2}' | cut -c1-4)
    do 
         ethtool -G $i rx $bufsize  > /dev/null 2>&1 
         ethtool -G $i tx $bufsize  > /dev/null 2>&1
         ethtool -K $i lro off > /dev/null 2>&1
         ip link set dev $i mtu 9000 2>&1
    done

echo "16777216" > /proc/sys/net/core/wmem_default
echo "16777216" > /proc/sys/net/core/rmem_default
echo "16777216" > /proc/sys/net/core/rmem_max
echo "16777216" > /proc/sys/net/core/wmem_max
echo "4096 87380 16777216" > /proc/sys/net/ipv4/tcp_rmem
echo "4096 87380 16777216" > /proc/sys/net/ipv4/tcp_wmem
echo "30000" > /proc/sys/net/core/netdev_max_backlog
echo "1" > /proc/sys/net/ipv4/tcp_mtu_probing
echo "1024" > /proc/sys/net/ipv4/tcp_base_mss
echo "htcp" > /proc/sys/net/ipv4/tcp_congestion_control
