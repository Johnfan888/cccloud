#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
        groupnamedata = {1: 'smtp', 2: 'dns', 3: 'tcp'}
	groupname_data = json.dumps(groupnamedata)
        print groupname_data
main()
