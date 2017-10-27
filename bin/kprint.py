#! /usr/bin/env python
# Copyright (C) 2017 Daniel Fava. All Rights Reserved.
import os
import sys
import xml.dom.minidom

def pprint(lines):
	strings = []
	for line in lines:
		if line[0] == '<':
			xml_string = line.replace("<-", "&lt;-")
			xmlh = xml.dom.minidom.parseString(xml_string)
			string = xmlh.toprettyxml()
			string = os.linesep.join([s for s in string.splitlines()[1:] if s.strip()])
			string = string.replace("&gt;", ">").replace("&lt;", "<")
			strings.append(string)
		else:
			strings.append(line.strip())
	return "".join(strings)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		f = open(sys.argv[1], 'r')
		print(pprint(f.readlines()))
	else:
		print(pprint(sys.stdin.readlines()))
