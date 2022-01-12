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
