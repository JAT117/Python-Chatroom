#!/usr/bin/env python3
"""
usage:  chmod u+x health_parser.py
	./health_parser.py <outputToParse.log>

	results stored in "report.log"
"""

import sys, os, re
from pathlib import Path

data_folder = Path("/root/python_scripts/")
temp = data_folder/"temp.txt"

empty_lines_removed = []

commandKeys=['salt *Controller* cmd.run clustercheck', \
'df -kh', \
'salt * cmd.run ceph health', \
'heat stack-list', \
'ironic node-list', \
'nova list', \
'nova service-list', \
'ntpstat', \
'ntpq -p', \
'salt *Controller* cmd.run ntpq -p', \
'salt * cmd.run df -kh', \
'salt *Controller* cmd.run ntpstat', \
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


"""
#cbam commands currently ignored#
read SSHCBAM
$SSHCBAM  /bin/bash << EOF
systemctl status cbam-reconfigure.service
nslookup google.com
ntpq -p
systemctl status cbam-operability-distribution.service
sudo systemctl status cbam-component-catalog.service
sudo systemctl status cbam-component-alma.service
sudo systemctl status cbam-scheduler.service
exit
EOF
"""

successKeys=['HTTP/1.1 200 OK', \
'power on', \
'HEALTH_OK' \
'active', \
'ACTIVE', \
'Loaded: Active', \
'Running', \
'UPDATE_COMPLETE', \
'up', \
'enabled', \
'synchronised to NTP server', \
':-)']

failKeys=['ssh: connect to host', \
'HEALTH_WARN', \
'NONE', \
'down', \
'xxx', \
'Loaded: inactive', \
'command not found']



def successful_case(parse_list,x):
	print("Test Case succeeded: {}\n".format(parse_list[0]))
	report_line = "{} :\n".format(parse_list[0])
	for element in parse_list:
		if x == element:
			pos = (parse_list.index(element) - 1)
			noun  = parse_list[pos]
			report_line += "{} {} \n".format(noun, element)
		else:
			pass

	return report_line


def fail_case(parse_list, error):
	print("Test Case failed: {}\n".format(parse_list[0]))
	report_line = "{}:\n".format(parse_list[0])
	for element in parse_list:
		if x == element:
			pos = (parse_list.index(element) - 1)
			noun  = parse_list[pos]
			report_line += "{} {}".format(noun, element)
		else:
			pass

	return report_line





def pass_fail_check(parse_list=[]):
	test_case=""
	#print("Performing pass/fail check\n")
	for x in parse_list:
		if (x in successKeys):
			print("{} found successfully".format(x))
			test_case = successful_case(parse_list,x)

		elif (x in failKeys):
			print("{} reported as failure".format(x))
			test_case = fail_case(parse_list, x)

		else:
			pass #print("Could not determine if test case passed or failed")
		
	return test_case


def load_buffer(key1, key2, empty_lines_removed):
	#print("Loading Buffer\n")
	start = key1
	end = key2
	buf = []
	log = False
	for line in empty_lines_removed:
		if line.startswith(start):
			buf.append(line.strip())
			log = True
		elif line.startswith(end):
			log = False
		elif log:
			buf.append(line.strip())
	return buf


def parse_file(empty_lines_removed):
	#print("Parsing File\n")
	with open("report.log", "a") as rp:
		for line in empty_lines_removed:
			to_parse = []
			if ((line in commandKeys) and (line != commandKeys[-1])):
				#print("\"{}\" in commandKeys".format(line))
				buf_start_string = line
				#print("buf_start_string: {}".format(buf_start_string))
				pos = (commandKeys.index(line)) + 1
				buf_end_string = commandKeys[pos]
				#print("buf_end_string: {}\n".format(buf_end_string))
				to_parse = load_buffer(buf_start_string, buf_end_string, empty_lines_removed)
				parsed_case = pass_fail_check(to_parse)
				rp.write(parsed_case)
				continue
			elif (line == commandKeys[-1]):
				to_parse = load_buffer(line, empty_lines_removed[-1], empty_lines_removed)
				parse_cased=pass_fail_check(to_parse)
				rp.write(parsed_case)
				continue
			else:
				pass
				#print("\"{}\" not in commandKeys".format(line))


def main(input_file):
	print("Starting parser on file {}".format(input_file))
	if (os.path.exists(input_file) == True):
		raw = open(input_file)
		lines = raw.readlines()
		raw.close()
		for line in lines:
			empty_lines_removed.append(line.strip())
		parse_file(empty_lines_removed)
		print("Parsing complete, results stored in report.log. Exiting Program\n")
		exit()
	else:
		print("File {} Not Found, Exiting Program".format(input_file))


if __name__ == "__main__":
	main(input_file = sys.argv[1])
