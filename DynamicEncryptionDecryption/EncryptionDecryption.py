#!/usr/bin/python3

"""
Created on Wed Aug 03 15:34:06 2016

@author: RAVI TEJA AINAMPUDI
"""
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto import Random
import os, random, sys


class DynamicEncryptionAndDecryption(object):
    def __init__(self, filename=None):
        self.filename = filename

    def encrypt(self, key, filename):
        chunksize = 128 * 1024
        outFile = os.path.join(os.path.dirname(filename), "(Secured)" + os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(AES.block_size)
        print(IV, len(IV))
        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, "rb") as infile:
            with open(outFile, "wb") as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))
                    outfile.write(encryptor.encrypt(chunk))
        return outFile

    def decrypt(self, key, filename):
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

    @staticmethod
    def allfiles(path=os.getcwd()):
        allFiles = []
        for root, subfiles, files in os.walk(path):
            for dir_name in subfiles:
                allFiles.append(os.path.join(root, dir_name))
            for file_name in files:
                allFiles.append(os.path.join(root, file_name))
        return allFiles


def choices():
    ed_object = DynamicEncryptionAndDecryption()
    choice = input("Do you want to L - List the Files, E - Encrypt or D - Decrypt? ==")
    print("\n")
    perform_multiple_encryption = input(f"Do you want to perform multi-layered encryption? Y-Yes or N-No: ")
    if perform_multiple_encryption.lower() not in ("yes", "y"):
        perform_multiple_encryption = False
        password = input("Please enter the `Password/Key` to be used: ")
    else:
        encFiles = ed_object.allfiles()

    if choice == "E":
        print("")
        subchoice = input("Want to encrypt all the Files ? Y- Yes or N - No ? :")
        if subchoice == "Y":
            for Tfiles in encFiles:
                if os.path.basename(Tfiles).startswith("(Secured)"):
                    print(f"{Tfiles} is already encrypted")
                    pass
                elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
                    pass
                else:
                    ed_object.encrypt(MD5.new(password).digest(), str(Tfiles))
                    print(f"Done Encryption for {Tfiles}")
                    os.remove(Tfiles)
        elif subchoice == "N":
            print("")
            filename = input("Enter the Filename to Encrypt: ")
            if not os.path.exists(filename):
                print(f"Given file {filename} does not exist")
                sys.exit(0)
            elif filename.startswith("(Secured)"):
                print(f"File {filename} was already encrypted")
                sys.exit()
            else:
                ed_object.encrypt(MD5.new(password).digest(), filename)
                print(f"Done Encryption of {filename}")
                os.remove(filename)
        else:
            print("\n Enter either Y or N")

    elif choice == "D":
        print("")
        filename = input("Enter the filename to decrypt: ")
        if not os.path.exists(filename):
            print(f"Given file {filename} does not exist")
            sys.exit(0)
        elif not filename.startswith("(Secured)"):
            print("{filename} file was never encrypted")
            sys.exit()
        else:
            ed_object.decrypt(MD5.new(password).digest(), filename)
            print(f"Done Decryption for {filename}")
            os.remove(filename)

    elif choice == "L":
        print(" \n The files present in the current directory are: ")
        file_list = []
        for content in os.listdir(".."):
            file_list.append(content)
        print(file_list)

    else:
        print("\n Please choose a valid command. Either E or D")
        sys.exit()


if __name__ == "__main__":
    ed = DynamicEncryptionAndDecryption()
    ed.encrypt(MD5.new(bytes("test".encode('utf-16be'))).digest(), "/home/osboxes/PycharmProjects/Dynamic-Encryption-And-Decryption-of-Any-files/random.txt")
    #choices()
