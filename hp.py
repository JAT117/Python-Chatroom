#!/usr/bin/env python3

import sys, os, re

empty_lines_removed = []

commandKeywordList=['source stackrc' \
'salt *ontroller* cmd.run clustercheck', \
'df -kh', \
'salt * cmd.run ceph health', \
'heat stack-list', \
'ironic node-list', \
'nova list', \
'nova service-list', \
'ntpstat', \
'ntpq -p', \
'salt *ontroller* cmd.run ntpq -p', \
'salt * cmd.run df -kh', \
'salt *ontroller* cmd.run ntpstat', \
'salt * cmd.run ntpstat', \
'salt * cmd.run hwclock --systohc', \
'source overcloudrc', \
'nova list --all --fields=host,name,status', \
'salt Controller-0 cmd.run sudo ceph osd tree', \
'nova service-list', \
'cinder service-list', \
'heat service-list |grep controller-0 | grep up |wc -l', \
'heat service-list', \
'salt * cmd.run free -h', \
'salt * cmd.run mpstat', \
'neutron agent-list', \
'sudo systemctl status ntpd', \
'salt Controller* cmd.run sudo pcs status', \
'salt * cmd.run sudo systemctl --failed | grep -i fail']

successKeywordList=['HTTP/1.1 200 OK', \
'power on', \
'HEALTH_OK' \
'active', \
'ACTIVE', \
'Running', \
'synchronised to NTP server']

failKeywordList=['No route to host','HEALTH_WARN']

def main(input_file):
	if (os.path.exists(input_file) == True):
		print("Parsing File: {}" .format(input_file))
		raw = open(input_file)
		lines = raw.readlines()
		raw.close()

		for line in lines:
			empty_lines_removed.append(line.strip())

		parse_file(empty_lines_removed)
		print("Parsing complete, results stored in report.log")
		exit()
	else:
		print("File {} Not Found, Exiting Program".format(input_file))


def parse_file(empty_lines_removed):
		with open("report.log", "a+") as rp:
			for line in empty_lines_removed:
				if line in commandKeywordList:
					rp.write(line+"\n")

if __name__ == "__main__":
	main(input_file = sys.argv[1])
