#!/usr/bin/env python3

import sys, os

commandKeyList=['source stackrc', \
' salt *ontroller* cmd.run clustercheck', \
' df -kh', \
' salt * cmd.run ceph health', \
' heat stack-list', \
' ironic node-list', \
' nova list', \
' nova service-list', \
' ntpstat', \
' ntpq -p', \
' salt *ontroller* cmd.run ntpq -p', \
' salt * cmd.run df -kh', \
' salt *ontroller* cmd.run ntpstat', \
' salt * cmd.run ntpstat', \
' salt * cmd.run hwclock --systohc', \
' source overcloudrc', \
' nova list --all --fields=host,name,status', \
' salt Controller-0 cmd.run sudo ceph osd tree', \
' nova service-list', \
' cinder service-list', \
' heat service-list |grep controller-0 | grep up |wc -l', \
' heat service-list', \
' salt * cmd.run free -h', \
' salt * cmd.run mpstat', \
' neutron agent-list', \
' sudo systemctl status ntpd', \
' salt Controller* cmd.run sudo pcs status', \
' salt * cmd.run sudo systemctl --failed | grep -i fail']

passKeyList=['HTTP/1.1 200 OK', \
'power on', \
'HEALTH_OK' \
'active', \
'ACTIVE', \
'Running', \
'synchronised to NTP server']

failKeyList=['No route to host','HEALTH_WARN']



def main(file):
	with open(file) as openFile:
		fileContents = openFile.read()
		print(fileContents)
		"""
		for line in fileContents:
			line.rstrip()
			if line in commandKeyList:
				print("{} is in the list".format(line))

			else:
				print("{} Not found in list".format(line))
		"""

if __name__ == "__main__":
        main(file = sys.argv[1])
