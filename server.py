import threading
import socket
from pyngrok import ngrok
import os


port=1234

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
server.bind(("",port))
server.listen(2)


public_url = ngrok.connect(port,"tcp")
print("ngrok tunnel \"{}\" -> \"tcp://127.0.0.1:{}\"".format(public_url, port))

clients=[]
names=[]


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            nickname=names[index]
            broadcast(f"{nickname} left".encode('ascii'))
            names.remove(nickname)

def recieve():
    while True:
        client,address=server.accept()
        print(f'Connected with {str(address)}')

        client.send('WHOISTHIS'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        names.append(nickname)
        clients.append(client)
        print(f'nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the server'.encode('ascii'))
        
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()


recieve()
