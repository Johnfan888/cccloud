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
    if form.has_key("floating_ip") and form["floating_ip"].value != "" and form["ins_id"].value != "":
        try:
                floatingip = form["floating_ip"].value
                ins_id = form["ins_id"].value
                instance = identify.nova.servers.get(ins_id)
                instance.add_floating_ip(floatingip)
                print "sucessful"
        except:
                print "openstack error"
    else:
        print "data error"
main()
