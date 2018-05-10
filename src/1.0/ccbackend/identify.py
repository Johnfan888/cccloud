import novaclient.v1_1.client as nvclient

import cinderclient.v2.client as cinderclient

import neutronclient.neutron.client as neutronclient

cinder = cinderclient.Client('demo','demo','istl','http://192.168.5.71:5000/v2.0')

#neutron = neutronclient.Client('demo','demo','istl','http://192.168.5.71:5000/v2.0')

nova = nvclient.Client('demo','demo','istl','http://192.168.5.71:5000/v2.0')
