# Container Security API for Dynamic Encryption And Decryption of files

This project provides a Python's FLASK API to perform Dynamic Encryption and Decryption of any file on OS File systems.

And it can be integrated into containers like Docker and Kubernetes. And it works perfectly fine on any virtual machine, compute instance or on-prem machine. 

# DynamicEncrptionDecryption

All the files in the folder are encrypted and decrypted, using a symmetric cipher.
Hashes contain dynamic keys driven by user to enhance security. 
Cipher block chaining and initialized vector were used for Python scripting. 
Operating system interface and System specific parameters were used accordingly. 

In this the Cipher used is AES and hash used is MD5. The other possible combinations which could be possible used are (AES , SHA256)  and (AES , MD4).  

The other possible combinations are also possible. Like  Cipher - DES3, RSA, Blowfish, ARC2, CAST, etc. 
And for Hash, like HMAC, SHA384, RIPEMD-160, etc.

Each combination needs to managed according to the key and the initialization vector requirements. 
Choose the combination such that Cipher block chaining, Key and Initialization vector are intact. 

# Key points to remember 

- Save and Run the code in a separate directory. Such that it doesn't effect your work flow. 

- You can use any key for this encryption. But make sure you use the same "KEY" for both the encryption and decryption. Or the end results may vary.

- Remember the key. If you forget the key. It is highly impossible to retrieve back your files. Because the AES is a beast. :boom:

- It is recommended to run this script on a "Virtual Machine".  

# For Mutiple Encryption and Decryption with this code
- Encryption can repeated by passing the subsequent filenames. 
- For decryption, make sure you keys in reverse order of what you have used for encryption.

# Docker Commands
To build the docker image:
> docker build -f Dockerfile -t hello-python:latest .

To run the docker container on background 
> docker run -d -p 5001:5000 hello-python


# Happy Encryption  :joy: :v:
# :no_pedestrians: :do_not_litter: Save your privacy :muscle: :metal:



