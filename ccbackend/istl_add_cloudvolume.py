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
    if form.has_key("ins_id") and form["ins_id"].value != "" and form["Cloudvolumename"].value != "":
	ins_id = form["ins_id"].value
	volume_id = form["Cloudvolumename"].value
        instance =identify.nova.servers.get(form["ins_id"].value)
	mountpoint = '/dev/vdb'
        try:
		identify.cinder.volumes.attach(volume=volume_id, instance_uuid=ins_id, mountpoint=mountpoint, mode='rw')
                print "sucessful"
        except:

                print "openstack error"
    else:
        print "fail"
main()
