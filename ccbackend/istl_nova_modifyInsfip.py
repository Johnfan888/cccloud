#!/usr/bin/python
import os
import time
import cgi
import urllib
import identify
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if form.has_key("ins_id") and form["ins_id"].value != "":
        ins_id = form["ins_id"].value
        instance = nova.servers.get(form["ins_id"].value)
        if form.has_key("floating_ip") and form["floating_ip"].value != "":
                try:
                        floatingip = form["floating_ip"].value
                        old_floatingip = form["old_floating_ip"].value
                        identify.nova.servers.remove_floating_ip(ins_id,old_floatingip)
                        instance.add_floating_ip(floatingip)
                        print "sucessful"
                except:
                        print "fail"

    else:
        print "data error"

main()
