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
        if form.has_key("ins_newname") and form["ins_newname"].value != "":
                try:
			name = form["ins_newname"].value
			identify.nova.servers.update(server=ins_id, name=name)
                        print "sucessful"
                except:

                        print "fail"
        else:
                print "fail"
        
        if form.has_key("flavor") and form["flavor"].value != "":
                try:
			flavor = form["flavor"].value
                        identify.nova.servers.resize(server=ins_id,flavor=flavor,disk_config="AUTO")
                        print "sucessful"
                except:
                        print "fail"
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
