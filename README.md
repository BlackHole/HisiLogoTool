If you lost the boot logo and want it back:

upload (FTP) logo.img attached into /tmp 

telnet/ssh: 

dd if=/tmp/logo.img of=/dev/block/by-name/logo 

- To save original logo.img use command  
dd if=/dev/block/by-name/logo of=/tmp/logo.img 

- To strip the dumped file: 
strip.py logo.img 

- To convert the extracted logo to jpeg: 
hisi2jpeg.py logo.img 

- To convert your own jpeg logo to hisi format:  
jpeg2hisi.py logo.jpg
