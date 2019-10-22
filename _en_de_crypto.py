#!/usr/bin/python
# File Encryption Service with password protection.
# Description : 
# this project is to create a solution to encrypte my pesonal data with password protection.
# I am not interested to use any third party apps or service for this task.
# @author - Praveen Veera
# mail - praveenveera92@gmail.com
################################################################
import sys
import os
import base64
import datetime
from datetime import datetime
from Crypto.Cipher import AES
from Crypto import Random

def key_gen():
    key = Random.new().read(AES.block_size)
    iv = Random.new().read(AES.block_size)
    return key,iv
 
def read_file(filename,path):
    '''func to read the data from the file'''
    if (filename != '_en_de_crypto'):
	    with open(path+"/"+filename,'r') as file:
	        data=file.read()
	    return data

def en_code(key,iv,data):
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    en_data = cfb_cipher.encrypt(data)
    return en_data

def write_file(filename,data,path):
    with open(path+"/"+filename,'w') as file:
        file.write(data) 

def de_code(key,iv,data):
    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    de_data = cfb_decipher.decrypt(data)
    return de_data

def input_en_de_check():
    input_argv_read = raw_input('Enter the function : ')
    if input_argv_read == 'en':
        return 1
    elif input_argv_read == 'de':
        return 0
    else:
        print('specified input does not match')
        exit()

def wrk_dir():
    '''func to get the current working directory'''
    dirname = os.path.realpath(os.path.dirname(sys.argv[0]))
    print ("Directory : ", dirname)
    return  dirname

def base_file(file):
    base_file, _ext = os.path.splitext(file)
    return base_file

def file_rename(base,ext):
    re_file= base+'.'+ext
    return re_file

def file_remove(file,path):
    os.remove(path+"/"+file)
    return True

def main():
    _en_de_check = input_en_de_check()
    path = wrk_dir()
    key_file = 'cipher.key'
    iv_file =  'salt.iv'
    if _en_de_check == 1 :
        key,iv = key_gen()
        for file in os.listdir(path):
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                data = read_file(file,path)
                en_data = en_code(key,iv,data)
                base= base_file(file)
                op_file = file_rename(base,'enc')
                print (op_file)
                write_file(op_file,en_data,path)
                write_file(key_file,key,path)
                write_file(iv_file,iv,path)
                file_remove(file,path)
    
    elif _en_de_check == 0 :
        for file in os.listdir(path):
            base= base_file(file)
            key = read_file(key_file,path)
            iv = read_file(iv_file,path)
            if file.endswith(".enc"):
                data = read_file(file,path)
                de_data = de_code(key,iv,data)
                op_file = file_rename(base, 'jpg')
                print (op_file)
                write_file(op_file,de_data,path)
                file_remove(file,path)
    else : 
        print("input validation failed")

if __name__ == "__main__":
    main()
