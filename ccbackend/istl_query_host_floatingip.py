#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	floatingip_list3 = identify.nova.floating_ips.list()
	i3 = 1
	float_dict = {}
	for i in floatingip_list3:
        	floatingstr = str(i).split()
        	if len(floatingstr[3]) < 20:
                	floatingip = floatingstr[4]
               		float_dict[i3] = floatingip[3:-1]
                	i3=i3+1
        float_data = json.dumps(float_dict)
        print float_data
main()
