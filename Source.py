#!usr/bin/env python
#coding:utf-8

import sys
import struct
import binascii

def checkMagicNumber(f,begin):
        flag=False
        magic_number, = struct.unpack("!L",c[begin:begin+4])
        magic_number=hex(magic_number)[2:-1]
        if magic_number=="cafebabe":
                flag=True
        return flag,begin+4

def getVersion(f,begin):
        minor_version, = struct.unpack("!H",c[begin:begin+2])
        major_version, = struct.unpack("!H",c[begin+2:begin+4])
        return minor_version,major_version,begin+4

def getCONSTANT_Pool_count(f,begin):
        CONSTANT_Pool_Count, = struct.unpack("!H",c[begin:begin+2])
        return CONSTANT_Pool_Count



if __name__=="__main__":
        #filepath=raw_input("Please input the filepath:")
        filepath=r"helloworld.class"
        try:
                f=open(filepath,"rb")
                c=f.read()
                f.close()
        except Exception, e:
                print "Unable to open the file."
                sys.exit()
        flag,fPointer=checkMagicNumber(f,0)
        if flag==False:
                print "Not a Java Class File!"
                sys.exit()
        print "Java Class File detected!(cafebabe)"

        minor_version,major_version,fPointer = getVersion(f,fPointer)
        print "minor_version:",minor_version,"major_version:",major_version

        CONSTANT_Pool_Count = getCONSTANT_Pool_count(f,fPointer)
        print "CONSTANT_Pool_Count:",CONSTANT_Pool_Count

        
