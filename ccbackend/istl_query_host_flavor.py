#!/usr/bin/python
import identify
import cgi
import urllib
import json
def main():
        print "Content-type: text/html\n"
	
	flavor_list = identify.nova.flavors.list()
	i0=1
	flavor_dict = {}
	for flavor in flavor_list:
        	flavorstr = str(flavor)
        	flavor_dict[i0] = flavorstr[9:-1]
       	 	i0=i0+1
        flavor_data = json.dumps(flavor_dict)
        print flavor_data
main()
