# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 15:34:06 2016

@author: RAVI TEJA AINAMPUDI
"""
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import os, random, sys
 
def encrypt(key, filename):
        chunksize = 128 * 1024
        outFile = os.path.join(os.path.dirname(filename), "(Secured)"+os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = ''
 
        for i in range(16):
                IV +=  chr(random.randint(0, 0xFF))
       
        encryptor = AES.new(key, AES.MODE_CBC, IV)
 
        with open(filename, "rb") as infile:
                with open(outFile, "wb") as outfile:
                        outfile.write(filesize)
                        outfile.write(IV)
                        while True:
                                chunk = infile.read(chunksize)
                               
                                if len(chunk) == 0:
                                        break
 
                                elif len(chunk) % 16 !=0:
                                        chunk += ' ' *  (16 - (len(chunk) % 16))
 
                                outfile.write(encryptor.encrypt(chunk))
 
 
def decrypt(key, filename):
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[9:]))
        chunksize = 128 * 1024
        with open(filename, "rb") as infile:
                filesize = infile.read(16)
                IV = infile.read(16)
 
                decryptor = AES.new(key, AES.MODE_CBC, IV)
               
                with open(outFile, "wb") as outfile:
                        while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                        break
 
                                outfile.write(decryptor.decrypt(chunk))
 
                        outfile.truncate(int(filesize))
       
def allfiles():
        allFiles = []
        for root, subfiles, files in os.walk(os.getcwd()):
                for names in files:
                        allFiles.append(os.path.join(root, names))
 
        return allFiles
 
print ""      
choice = raw_input("Do you want to L - List the Files, E - Encrypt or D - Decrypt? ==")
print ""
password = raw_input("Please enter the `Password/Key` to be used: ")
 
encFiles = allfiles()
 
if choice == "E":
        print ""
        subchoice = raw_input("Want to encrypt all the Files ? Y- Yes or N - No ? ")
        if subchoice == "Y":
          for Tfiles in encFiles:
                if os.path.basename(Tfiles).startswith("(Secured)"):
                        print "%s is already encrypted" %str(Tfiles)
                        pass
 
                elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
                        pass
                else:
                        encrypt(MD5.new(password).digest(), str(Tfiles))
                        print "Done Encryption %s" %str(Tfiles)
                        os.remove(Tfiles)
 
        elif subchoice == "N":
            print ""
            filename = raw_input("Enter the Filename to Encrypt: ")
            if not os.path.exists(filename):
                print "Given file does not exist"
                sys.exit(0)
            elif filename.startswith("(Secured)"):
                print "%s was already encrypted" %filename
                sys.exit()
            else:
                encrypt(MD5.new(password).digest(), filename)
                print "Done Encryption %s" %filename
                os.remove(filename)
            
        else:
            print ""
            print "Enter either Y or N" 
 
elif choice == "D":
          print ""
               
          filename = raw_input("Enter the filename to decrypt: ")
          if not os.path.exists(filename):
                print "Given file does not exist"
                sys.exit(0)
          elif not filename.startswith("(Secured)"):
                print "%s is was never encrypted" %filename
                sys.exit()
          else:
                decrypt(MD5.new(password).digest(), filename)
                print "Done Decryption %s" %filename
                os.remove(filename)

elif choice == "L":
        print ""
        print "The files present in the current directory are:"
        file_list = []
        for content in os.listdir("."):
            file_list.append(content)
        print file_list
        
else:
        print ""
        print "Please choose a valid command. Either E or D"
        sys.exit()
