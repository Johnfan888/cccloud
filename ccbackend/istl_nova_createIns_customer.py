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
    if form.has_key("ins_name") and form["ins_name"].value != "" and form["image"].value != "":
        try:
                ins_name = form["ins_name"].value
                image_data = form["image"].value
                image = identify.nova.images.find(name=image_data)
                flavor_data = form["flavor"].value
                flavor = identify.nova.flavors.find(name=flavor_data)
                key_name = form["key_name"].value
		file_data = form["filedata"].value
                instance = identify.nova.servers.create(name = ins_name, image=image, flavor=flavor, key_name=key_name,nics=[{'net-id':'6903911e-f85b-4b55-aae8-26ed1d7ff857'}],disk_config="AUTO",config_drive="True",files={"/etc/init.d/meta.sh":file_data},meta={"name":"liang"},admin_pass="lixiao")
                #while status == 'BUILD': 
                #        time.sleep(5)
                ins_id = instance.id
                #instance = identify.nova.servers.get(ins_id)
                #instance.add_floating_ip(floatingip)
                print ins_id 
        except:
                print "openstack error"
    else: 
        print "data error"
main()

