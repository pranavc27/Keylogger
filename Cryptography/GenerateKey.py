from cryptography.fernet import Fernet


file_path = "D:\\python programs\\advanced keylogger\\Cryptography"
extend = "\\"
file_merge = file_path + extend

key = Fernet.generate_key()
with open( file_merge+ "encryption_key.txt", 'wb') as f:

    f.write(key)
    f.close()