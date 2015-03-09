#!usr/bin/env python
#coding:utf-8

import sys
import struct
import binascii

def checkMagicNumber(f,begin):
        flag=False
        magic_number, = struct.unpack("!L",c[begin:begin+4])
        magic_number=hex(magic_number)[2:-1]
        print magic_number
        if magic_number=="cafebabe":
                flag=True
        return flag,begin+4

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
        print "Java Class File detected!"

        
