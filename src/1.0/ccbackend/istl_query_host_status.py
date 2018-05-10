#!/usr/bin/python
import cgi
import urllib
import json
import identify
def main():
        print "Content-type: text/html\n"
    	form = cgi.FieldStorage()
    	if form.has_key("ins_id") and form["ins_id"].value != "" :
        	try:
                	ins_id = form["ins_id"].value
                	instance = identify.nova.servers.get(ins_id)
                	status = instance.status
                	print status
        	except:
                	print "openstack error"
    	else:
        	print "data error"
main()
