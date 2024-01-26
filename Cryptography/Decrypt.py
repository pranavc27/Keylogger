from cryptography.fernet import Fernet


file_path = "D:\\python programs\\advanced keylogger\\Project"
extend = "\\"
file_merge = file_path + extend


key = "S0OeV5YOL8Qgn6wJjbI3PLTg0Le_EpRf80M6uZp698Y="

system_information_e ="e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_key_log.txt"


encrypted_files = [file_merge + system_information_e , file_merge + clipboard_information_e , file_merge + keys_information_e]

count =0

for decrypting in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open (encrypted_files[count] , 'wb') as f:
        f.write(decrypted)

    
    count += 1