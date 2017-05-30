#!/opt/murmanov/bin/python
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import textfsm

switchlist = "../F10-MXL-FULL"

result = ""
hostnames = [line.rstrip('\n') for line in open(switchlist)]

for hostname in hostnames: 

	CISCO = {
    'device_type': 'cisco_ios',
    'ip':   hostname ,
    'username': 'ansible',
    'password': 'ansiblehost',
	}

	try:
		net_connect = ConnectHandler(**CISCO)
		output = net_connect.send_command('show inventory | i NAME|PID')
		net_connect.disconnect()
		encodedoutput = output.encode("utf-8")
		template = open("show_inventory_multiple.textfsm")
		re_table = textfsm.TextFSM(template)
		fsm_results = re_table.ParseText(encodedoutput)
		# the results are written to a CSV file
		outfile_name = open("outfile-for-"+hostname+".csv", "w+")
		outfile = outfile_name

		# Display result as CSV and write it to the output file
		# First the column headers...
		#print(re_table.header)
		for s in re_table.header:
		    outfile.write("| %s " % s)
		outfile.write("|\n")
		
		# ...now all row's which were parsed by TextFSM
		counter = 0
		for row in fsm_results:
		#    print(row)
		    for s in row:
		        outfile.write("| %s " % s)
		    outfile.write("|\n")
		    counter += 1

		print("Write %d records" % counter)
		connected = True
	except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        	result = result+("{}\n".format(e))
        	connected = False
