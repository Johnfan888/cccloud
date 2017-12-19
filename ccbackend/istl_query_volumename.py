#!/usr/bin/python
import cgi
import urllib
import identify
import json
def main():
        print "Content-type: text/html\n"
	avail_vol_list = identify.cinder.volumes.list(search_opts={"status":"available"},sort_key="size",detailed="True")
	i4=1
	volume_dict = {}
	for volume in avail_vol_list:
        	volumestr = str(volume)
        	volume_dict[i4] = volumestr[9:-1]
        	i4=i4+1
        volumename_data = json.dumps(volume_dict)
        print volumename_data
main()
