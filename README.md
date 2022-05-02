If you lost the boot logo and want it back:

upload (FTP) logo.img attached into /tmp 

telnet/ssh: 

dd if=/tmp/logo.img of=/dev/block/by-name/logo 


To save original logo.img use command dd if=/dev/block/by-name/logo of=/tmp/logo.img
