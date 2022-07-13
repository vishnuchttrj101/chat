import socket
import threading
import tkinter
import pyautogui as pag
from tkinter import messagebox

addr=input("Input the server's address:")
ur=addr.split(":")[0]
PORT=int(addr.split(":")[1])
nickname=input("Please choose a nickname for you: ")
HOST=socket.gethostbyname(ur)


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))





def recieve():
    while True:
        try:
            message=client.recv(1024).decode('ascii')
            if message=='WHOISTHIS':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showinfo("Title", message)
                root.update()
                
        
        except:
            print("An error occured")
            client.close()
            break




def write():
    while True:
        message=f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))



recieve_thread=threading.Thread(target=recieve)
recieve_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()

