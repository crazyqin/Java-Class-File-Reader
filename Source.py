#!usr/bin/env python
#coding:utf-8

import sys
import struct
import binascii

class CONSTANT_Utf8_info():
        def __init__(self,length,string):
                self.length=length
                self.string=string

class CONSTANT_Integer_info():
        pass

class CONSTANT_Float_info():
        pass

class CONSTANT_Double_info():
        pass

class CONSTANT_Long_info():
        pass

class CONSTANT_Class_info():
        def __init__(self,i):
                self.i=i

class CONSTANT_String_info():
        def __init__(self,i):
                self.i=i

class CONSTANT_Fieldref_info():
        def __init__(self,i1,i2):
                self.i1=i1
                self.i2=i2

class CONSTANT_Methodref_info:
        def __init__(self,i1,i2):
                self.index1=i1
                self.index2=i2
class CONSTANT_InterfaceMethodref_info():
        pass

class CONSTANT_NameAndType_info():
        def __init__(self,i1,i2):
                self.i1=i1
                self.i2=i2

class CONSTANT_MethodHandle_info():
        pass

class CONSTANT_MethodType_info():
        pass

class CONSTANT_InvokeDynamic_info():
        pass

def checkMagicNumber(f,begin):
        flag=False
        magic_number, = struct.unpack("!L",f[begin:begin+4])
        magic_number=hex(magic_number)[2:-1]
        if magic_number=="cafebabe":
                flag=True
        return flag,begin+4

def getVersion(f,begin):
        minor_version, = struct.unpack("!H",f[begin:begin+2])
        major_version, = struct.unpack("!H",f[begin+2:begin+4])
        return minor_version,major_version,begin+4

def getAccess_flags(f,begin):
        access_flags, = struct.unpack("!H",f[begin:begin+2])
        flags=""
        if access_flags&1==1:
                flags=flags+",ACC_PUBLIC"
        if access_flags&16==16:
                flags=flags+",ACC_FINAL"
        if access_flags&32==32:
                flags=flags+",ACC_SUPER"
        if access_flags&512==512:
                flags=flags+",ACC_INTERFACE"
        if access_flags&1024==1024:
                flags=flags+",ACC_ABSTRACT"
        if access_flags&4096==4096:
                flags=flags+",ACC_SYNTHETIC"
        if access_flags&8192==8192:
                flags=flags+",ACC_ANNOTATION"
        if access_flags&16384==16384:
                flags=flags+",ACC_ENUM"
        return flags[1:],begin+2

def getThis_class(f,begin):
        this_class,=struct.unpack("!H",f[begin:begin+2])
        return this_class,begin+2

def getSuper_class(f,begin):
        super_class,=struct.unpack("!H",f[begin:begin+2])
        return super_class,begin+2        

def getCount(f,begin):       
        count, = struct.unpack("!H",f[begin:begin+2])
        return count,begin+2

def createCONSTANT_info(pool_count,f,begin):
        tag,=struct.unpack("B",f[begin:begin+1])
        #print tag
        if tag==12:
                i1,i2=struct.unpack("!HH",f[begin+1:begin+5])
                CONSTANT_info_list[pool_count]=CONSTANT_NameAndType_info(i1,i2)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                CONSTANT_info_ref[i1]=0
                CONSTANT_info_ref[i2]=0
                return tag,begin+5

        if tag==10:
                i1,i2=struct.unpack("!HH",f[begin+1:begin+5])
                CONSTANT_info_list[pool_count]=CONSTANT_Methodref_info(i1,i2)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                CONSTANT_info_ref[i1]=0
                CONSTANT_info_ref[i2]=0
                return tag,begin+5

        if tag==9:
                i1,i2=struct.unpack("!HH",f[begin+1:begin+5])
                CONSTANT_info_list[pool_count]=CONSTANT_Fieldref_info(i1,i2)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                CONSTANT_info_ref[i1]=0
                CONSTANT_info_ref[i2]=0
                return tag,begin+5

        if tag==8:
                i1,=struct.unpack("!H",f[begin+1:begin+3])
                CONSTANT_info_list[pool_count]=CONSTANT_String_info(i1)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                CONSTANT_info_ref[i1]=0
                return tag,begin+3

        if tag==7:
                i1,=struct.unpack("!H",f[begin+1:begin+3])
                CONSTANT_info_list[pool_count]=CONSTANT_Class_info(i1)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                CONSTANT_info_ref[i1]=0
                return tag,begin+3

        if tag==1:
                length,=struct.unpack("!H",f[begin+1:begin+3])
                #get the string from CONSTANT_Utf8_info as string
                string=""
                CONSTANT_info_list[pool_count]=CONSTANT_Utf8_info(length,string)
                if CONSTANT_info_ref[pool_count]==None:
                        CONSTANT_info_ref[pool_count]=1
                return tag,begin+3+length

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
        flag,fPointer=checkMagicNumber(c,0)
        if flag==False:
                print "Not a Java Class File!"
                sys.exit()
        print "Java Class File detected!(cafebabe)"

        minor_version,major_version,fPointer = getVersion(c,fPointer)
        print "minor_version:",minor_version,"major_version:",major_version

        CONSTANT_Pool_Count,fPointer = getCount(c,fPointer)
        print "CONSTANT_Pool_Count:",CONSTANT_Pool_Count

        CONSTANT_info_list=[None]*CONSTANT_Pool_Count
        CONSTANT_info_ref=[None]*CONSTANT_Pool_Count


        #constant pool
        pool_count = 1
        while(pool_count<CONSTANT_Pool_Count):
                tag,fPointer=createCONSTANT_info(pool_count,c,fPointer)
                pool_count=pool_count+1
        print CONSTANT_info_list,CONSTANT_info_ref

        access_flags,fPointer=getAccess_flags(c,fPointer)
        print "access_flags:",access_flags

        this_class,fPointer=getThis_class(c,fPointer)
        print "this_class:",this_class

        super_class,fPointer=getSuper_class(c,fPointer)
        print "super_class:",super_class

        interfaces_count,fPointer=getCount(c,fPointer)
        print "interfaces_count:",interfaces_count
        if interfaces_count!=0:
                print "Interfaces_count!=0"
                sys.exit()

        fields_count,fPointer=getCount(c,fPointer)
        print "fields_count:",fields_count
        if fields_count!=0:
                print "fields_count!=0"
                sys.exit()

        attributes_count,fPointer=getCount(c,fPointer)
        print "attributes_count:",attributes_count
        if attributes_count!=0:
                pass

