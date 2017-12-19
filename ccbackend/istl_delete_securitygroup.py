#!/usr/bin/python
import os
import time
import cgi
import urllib
import identify
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if form.has_key("ins_id") and form["ins_id"].value != "" and form["Securitygroupname"].value != "":
        ins_id = form["ins_id"].value
        instance = identify.nova.servers.get(form["ins_id"].value)
        security_group_id = form["Securitygroupname"].value
        try:
                #identify.nova.security_groups.find(name = "li-xiao")   
                instance.remove_security_group(security_group=security_group_id)
                print "sucessful"
        except:

                print "openstack error"
    else:
        print "fail"
main()
