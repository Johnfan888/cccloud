#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	sec_list = identify.nova.security_groups.list()
	i5 =1
	sec_dict = {}
	for secgrp in sec_list:
        	secgrpstr = str(secgrp)
        	sec_dict[i5] = secgrpstr
        	i5=i5+1
        sec_data = json.dumps(sec_dict)
        print sec_data
main()
