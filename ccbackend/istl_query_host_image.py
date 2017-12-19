#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	image_list = identify.nova.images.list()
	i1=1
	image_dict = {}
	for image in image_list:

        	imagestr = str(image)
       		if i1<=len(image_list):
                	image_dict[i1] = imagestr[8:-1]
        		i1=i1+1
        image_data = json.dumps(image_dict)
        print image_data
main()
