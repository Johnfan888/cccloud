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
		ins_id = form["ins_id"].value
		identify.nova.servers.suspend(server=ins_id)
                print "sucessful"
        except:
                print "openstack error"
		print ins_id

    else:
        print "fail"
main()
