**********控制节点*************
1、这些py脚本全部在控制节点上的web服务器的cgi-bin目录下，我的控制节点是suse虚拟机的/srv/www/cgi-bin/openstack目录下

example ：
    -rwxr-xr-x 1 wwwrun www 1293 Nov 17 09:17 istl_nova_createIns.py
	

   这些脚本的权限全部是755，文件用户是wwwrun   文件用户组是www

2、这些脚本文件都是调用openstackapi来完成的。