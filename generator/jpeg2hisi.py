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
	print( "Syntax: %s <logo.jpg>" % sys.argv[0])
	sys.exit(1)	

filename = sys.argv[1]
filesize = os.path.getsize(filename)

with open(filename, 'rb') as jpg:
	jpgdata = jpg.read(filesize)

	if jpgdata[6:10] != b'JFIF':
		print("File %s isn't a jpeg image" % filename)

	w = struct.unpack('>h', jpgdata[0xa5:0xa7])[0]
	h = struct.unpack('>h', jpgdata[0xa3:0xa5])[0]
	
	if "%dx%d" % (w,h) not in ["1920x1080", "1280x720"]:
		print("Format %dx%d not supported by hisi soc" % (w,h))
		sys.exit(1)	

	logo = open(os.path.splitext(filename)[0] + '.img2', 'wb')

	logo.write(HISI_HEADER)
	logo.write(b'\x00\x7c\x00\x00\x00')
	logo.write(MCE_LOGO_TABLENAME)
	logo.write(b'\x00' * 22)
	logo.write(b'\x50')
	logo.write(b'\x00' * 3)
	logo.write(MCE_LOGO_KEYNAME_FLAG)
	logo.write(b'\x00' * 19)
	logo.write(b'\x04')
	logo.write(b'\x00' * 3)
	logo.write(b'\x01')
	logo.write(b'\x00' * 3)
	logo.write(MCE_LOGO_KEYNAME_CONTLEN)
	logo.write(b'\x00' * 20)
	logo.write(b'\x04')
	logo.write(b'\x00' * 3)
	logo.write(struct.pack('<q', filesize)) #size
	logo.write(b'\x00' * (0x2000 - 0x80))
	logo.write(jpgdata)
	logo.close()

