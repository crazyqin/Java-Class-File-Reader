#!usr/bin/env python
#coding:utf-8

import sys
import struct
import binascii

#filepath=raw_input("Please input the filepath:")
filepath=r'helloworld.class'
try:
	f=open(filepath,'rb')
	c=f.read()
	f.close()
except Exception, e:
	print 'Unable to open the file.'
	sys.exit()
print c[0:4]
#magic_number=struct.unpack("I",c[0:4])
#print magic_number
