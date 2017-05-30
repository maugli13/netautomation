#!/opt/murmanov/bin/python
import paramiko
import time
import smtplib

vpnlist = "/opt/NetAutomation/vyos/VPN-LIST-FULL"

result = ""
hostnames = [line.rstrip('\n') for line in open(vpnlist)]


def disable_paging(contact_shell):
    '''Disable paging'''
    contact_shell.send("set terminal length 0\n")
    time.sleep(1)
    output = contact_shell.recv(1000)
    return output

if __name__ == '__main__':

	for vpnserver in hostnames:

    		username = 'vyos'
    		password = 'vyos'

    		contact = paramiko.SSHClient()
    		contact.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    		contact.connect(vpnserver, username=username, password=password, look_for_keys=False, allow_agent=False)
    		contact_shell = contact.invoke_shell()

    		output = contact_shell.recv(1000)

    		# Turn off paging
    		disable_paging(contact_shell)

    		contact_shell.send("\n")
    		contact_shell.send("show configuration commands > /config/"+vpnserver+"\n")
		contact_shell.send("copy file running://config/"+vpnserver+" to ftp://vyos:vyos@ftpserver.local/config/"+vpnserver+"\n") 
    		time.sleep(5)

    		output = contact_shell.recv(1000000)
		result = result+(vpnserver+" done!\n")

#SMTP 
addr = ['user1@example.com','user2@example.com']
smtpObj = smtplib.SMTP('mail.int', 25)
smtpObj.sendmail('vyos-backup@devbox.local', addr, 'Subject: Backup completed\n'+result)
smtpObj.quit()
