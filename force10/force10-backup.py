#!/opt/murmanov/bin/python
from netmiko import ConnectHandler
import smtplib
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

switchlist = "/opt/NetAutomation/F10-MXL-FULL"

result = ""
hostnames = [line.rstrip('\n') for line in open(switchlist)]

for hostname in hostnames: 

	Force10MXL = {
    'device_type': 'dell_force10',
    'ip':   hostname ,
    'username': 'user',
    'password': 'password',
	}

	try:
		net_connect = ConnectHandler(**Force10MXL)
		output = net_connect.send_command('copy run ftp://user:password@ftpserver.local/config/'+hostname)
		result = result+(hostname+" done!\n")
		net_connect.disconnect()
		connected = True
	except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        	result = result+("{}\n".format(e))
        	connected = False

#SMTP 
addr = ['user1@example.com','user2@example.com']
smtpObj = smtplib.SMTP('mail.int', 25)
smtpObj.sendmail('force10-backup@devbox.local', addr, 'Subject: Backup completed\n'+result)
smtpObj.quit()
