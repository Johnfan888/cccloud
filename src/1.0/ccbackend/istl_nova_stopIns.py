#!/usr/bin/python
import os
import time
import random
import cgi
import urllib
import identify
import json
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if form.has_key("ins_id") and form["ins_id"].value != "":
        try:	
		server = form["ins_id"].value
                identify.nova.servers.stop(server=server)
		print "sucessful"
        except:
                print "openstack error"

    else:
        print "data fail"
main()
