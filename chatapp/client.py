import socket
import threading

HEADER=64
PORT=1234
# SERVER='192.168.29.95'
SERVER=socket.gethostbyname(socket.gethostname()) #it does same as above so no hardcored as above
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT="DISCONNECTED..!"

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
print("waana get out of chat room? type: DISCONNECT")
name=input("username: ")
# msssg=''
client.send(name.encode(FORMAT))


def listen():
    
    connected =True
    while connected:
        
        m=client.recv(2048).decode(FORMAT)
        # print(f'expection msg: {m}')
        if m!='':
            print(f'{m}')
        else:
            print("msg received is empty")
            break
        
def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length+= b' ' * (HEADER - len(send_length))
    client.send(send_length)

def write_msg():
    while True:
        mssg=f'{input("")}'
        send(mssg)
        client.send(mssg.encode(FORMAT))

threading.Thread(target=listen).start()
threading.Thread(target=write_msg).start()