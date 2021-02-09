#!/usr/bin/env python3

list=['string1' ,'string 2', 'the third string']

list2=['string1', 'string2', 'the third string']

for x in list:
	if x in list2:
		print("{} is in list2".format(x))
	else:
		print("{} is NOT in list2".format(x))
