#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	key_list = identify.nova.keypairs.list()
	i2=1
	key_dict = {}
	for key in key_list:
        	keystr = str(key)
        	if i2<=len(key_list):
                	key_dict[i2] =keystr[10:-1]
        	i2 = i2+1
        key_data = json.dumps(key_dict)
        print key_data
main()
