import socket
import threading 
#creating multiple threads in one pyhton program so that if one thread is waiting o rthat code is not running then other can run
HEADER=64 #it means that first msg should be of lenght 64 and formating to string
PORT=1234
# SERVER='192.168.29.95'
SERVER=socket.gethostbyname(socket.gethostname()) #it does same as above but get it so no hardcoded
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT="DISCONNECT"
#socket creation
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#af_inet(internet) for ipv4 and stream for streaming data
#BINDING TO THE ADDRESS
server.bind(ADDR)
active_clients=[]
#to particular client
def send_message_to_client(conn, message):
    try:
        # print(f"the empty msg: {message}")
        conn.send(message.encode(FORMAT))
    except:
        print(f"{conn} connection is disconnected or never got connected")

# Function to send any new message to all the clients that are connected

def send_messages_to_all(message):
    
    for user in active_clients:
        # print(user[1])
        # print(active_clients)
        send_message_to_client(user[1], message)

def send_except_own(conn,message):
    for user in active_clients:
        if user[1]!=conn:
            send_message_to_client(user[1],message)

def handle_client(conn,addr):#handle individual connections
    print(f"[NEW CONNECTION] {addr} connected.")
    print(f"connection: {conn}")
   
    username=conn.recv(HEADER).decode(FORMAT)
   
    # while username=''
    # if username!='':
    prompt_message = "SERVER~ " + f"{username} added to the chat"
    print("promt_message: " + prompt_message)

    active_clients.append((addr, conn))

    connected =True
    send_messages_to_all(prompt_message)
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)# have to put the bits of info we'll recieve ..receive msg lenght
        # print(msg_length)
        if int(msg_length)!=0:
            msg_length= int(msg_length) 
            msg=conn.recv(msg_length).decode(FORMAT)#RECEV THE actual message
            if msg ==DISCONNECT:
                disconnected=f'{addr}: {username} got disconnected'
                print(disconnected)
                send_messages_to_all(disconnected)
                connected=False
            else:
                final_msg = f'[{username}] : {msg}'
                print(f"[{username}] {msg}")
                send_except_own(conn,final_msg)

            

        else:
            print(f'msg is empty from {username}')
            error=f'{username} please dont leave msg empty...!'
            m=''
            send_except_own(conn,m)
            send_message_to_client(conn,error)
    conn.close()      
    active_clients.remove((addr, conn))
    # else:
    #     print('username is not entered')
    #     error_u='username cannot be empty'
    #     send_message_to_client(conn,error_u)
    # threading.Thread(target=listen_for_messages, args=(conn,addr,msg_length )).start()


def start(): #allows to start listening for connections,,,,handle new connections 
    server.listen()
    print(f"[LISTENING] on {SERVER}")
    while True:
        conn, addr = server.accept()#wait for new connection and store the in conn and adrr for particular
        #conn is socket object that allows to comunicate back
        thread=threading.Thread(target=handle_client,args=(conn,addr))#starting thread of handle_client function
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")#-1 as start thread is already running

print("[starting] server is starting...")
start()