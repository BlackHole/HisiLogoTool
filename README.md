If you lost the boot logo and want it back:

upload (FTP) logo.img attached into /tmp 
telnet/ssh: 
dd if=/tmp/logo.img of=/dev/block/by-name/logo 
