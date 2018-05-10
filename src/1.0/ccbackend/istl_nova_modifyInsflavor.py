#!/usr/bin/python

import os
import time
import random
import cgi
import urllib
import identify
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if form.has_key("ins_id") and form["ins_id"].value != "" and form["flavor"].value != "":
        ins_id = form["ins_id"].value
	flavor_data = form["flavor"].value
        try:
		server = identify.nova.servers.get(ins_id)
		flavor = identify.nova.flavors.find(name=flavor_data)
                identify.nova.servers.resize(server=server,flavor=flavor,disk_config="AUTO")
		print "sucessful"
        except:
                print "openstack error"
    else:
        print "fail"
main()
