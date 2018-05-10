#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	net_list = identify.nova.networks.list()
	i6=1
	network_dict = {}
	for network in net_list:
        	networkstr = str(network)
        	network_dict[i6] = networkstr[10:-1]
        #print nova.networks.find(name = networkstr[10:-1])
        	i6=i6+1
        network_data = json.dumps(network_dict)
        print network_data
main()
