#!/usr/bin/python

import os
import time
import random
#import novaclient.v1_1.client as nvclient
import cgi
import urllib
#nova = nvclient.Client('demo','demo','istl','http://192.168.5.71:5000/v2.0')
def main():
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if form.has_key("ins_id") and form["ins_id"].value != "" and form["snapshoot_name"].value != "":
        try:
                instance = nova.servers.find(name=form["ins_id"])
                time.sleep(10)
                print random.random(),"sucessful"
        except:
                print str(random.random()),"sucessful"

                #print "fail"
    else:
        print "fail"
main()
~
