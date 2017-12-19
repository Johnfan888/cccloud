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
        newname = form["ins_newname"].value
        try:
		identify.nova.servers.update(server=ins_id, name=newname)
                print "sucessful"
        except:

                print "fail"
    else:
        print "data error"

main()
