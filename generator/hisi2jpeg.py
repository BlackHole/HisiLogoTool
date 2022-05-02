#! python3

# (c) openbh 2022

import sys
import os
import struct

HISI_HEADER = b"###"
MCE_LOGO_TABLENAME = b"LOGO_TABLE"
MCE_LOGO_KEYNAME_FLAG = b"LOGO_KEY_FLAG"
MCE_LOGO_KEYNAME_CONTLEN  = b"LOGO_KEY_LEN"

if len(sys.argv) == 1:
	print( "Syntax: %s <logo.img>" % sys.argv[0])
	sys.exit(1)	

filename = sys.argv[1]
if not os.path.exists(filename):
	print( "File %s doesn't exists" % filename)
	sys.exit(1)	

if os.path.getsize(filename) < 0x2000:
	print( "File %s is invalid" % filename)
	sys.exit(1)	
	
with open(filename, 'rb') as logo:
	header = logo.read(0x2000)
	if header[8:18] != MCE_LOGO_TABLENAME:
		print( "File %s is invalid" % filename)
		sys.exit(1)
	
	jpeg = open(os.path.splitext(filename)[0] + '.jpg', 'wb')
	data = logo.read(struct.unpack('<q', header[0x78:0x80])[0])
	jpeg.write(data)
	jpeg.close()
