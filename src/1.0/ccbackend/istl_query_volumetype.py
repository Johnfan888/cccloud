#!/usr/bin/python
import cgi
import urllib
import json
def main():
        print "Content-type: text/html\n"
        type_data = {1: '*', 2: '**', 3: '***', 4: '****'}
	typename = json.dumps(type_data)
        print typename
main()
