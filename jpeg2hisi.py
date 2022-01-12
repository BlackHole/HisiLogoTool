#! python3

# Copyright (C) Blackhole Team
# This file is part of HisiLogoTool <https://github.com/Blackhole/HisiLogoTool>.
#
# dogtag is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dogtag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dogtag.  If not, see <http://www.gnu.org/licenses/>.

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

	#https://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib
	size = 2
	ftype = 0
	pos = 0
	while not 0xc0 <= ftype <= 0xcf:
		pos += size
		byte = jpgdata[pos]
		#print ("%02x - %02x" % (byte,pos))
		pos+=1
		while byte == 0xff:
			byte = jpgdata[pos]
			pos+=1
			#print ("increment", pos, byte)
		ftype = byte
		size = struct.unpack('>H', jpgdata[pos:pos+2])[0] - 2
		pos+=2
	# We are at a SOFn block
	pos+=1 # Skip `precision' byte.
	h, w = struct.unpack('>HH', jpgdata[pos:pos+4])
	
	if "%dx%d" % (w,h) not in ["1920x1080", "1280x720"]:
		print("Format %dx%d not supported by hisi soc" % (w,h))
		sys.exit(1)	

	logo = open(os.path.splitext(filename)[0] + '.img', 'wb')

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

