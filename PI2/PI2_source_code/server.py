import socket
import time  
import threading
import csv
print("server starting up...")

#SERVER INFO
#TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 1234
FORMAT = 'utf-8'
DELAY = 5 # delay before another message is requested [seconds] 

#COMMANDS RECIEVED FROM SERVER
EXIT           = ('X').encode(FORMAT)
GET_STATUS     = ('S').encode(FORMAT)
GET_MESSAGE    = ('M').encode(FORMAT)

#CREATE FILE AND ARRAY
msgs = []
FILENAME = "/data/sensorlog.csv"
f = open(FILENAME, "a", newline="")
f.close()
#writer.writerow({'one','two','three'})

#FLAGS
#flag to determine Whether or not the server should request a message from the client
running = True
def sendOn():
    global running
    running = True
def sendOff():
    global running
    running = False
#flag to make sure a message and a status cannot be requested simultaneously
canRequest = True #true by defualt to send messages immediatly
def takeFlag(): #take flag
    global canRequest
    while not canRequest:
        time.sleep(0.5)
    canRequest = False
def returnFlag():#return flag
    global canRequest
    canRequest = True


#THREADED LOOP TO REQUEST A MESSAGE EVERY 'DELAY' SECONDS FROM THE CLIENT(PI1)
def sendCmds(s):
    while True:
        global getStatus
        global running
        if(running):
            takeFlag #take flag to ensure status and message cannot be requested simultaneously
            conn.send(GET_MESSAGE) #request message
            msgLen = int(ord(conn.recv(1).decode(FORMAT))) #get message length (always 1 byte)
            msg = conn.recv(msgLen).decode(FORMAT) #get message of specified length
            print("Message:",msg)
            time_sent = msg[0:8]
            temprature = msg[9:16]
            brightness = msg[18:]
            temp = [time_sent, temprature, brightness]#temporary formatted message
            f = open(FILENAME, "a", newline="") #open file and append new message
            writer = csv.writer(f) 
            writer.writerow(temp) #write message to file
            f.close()
            msgs.append("time: " + str(time_sent) + "  temprature: "+ str(temprature)+ " brightness: " + str(brightness))#store message to array
            returnFlag
            time.sleep(DELAY - 0.5) #delay the request for the next message
        time.sleep(0.5)

#CONNECT TO CLIENT
s = socket.socket()
s.bind(('', TCP_PORT))
s.listen(5)
try:
    conn, addr = s.accept() 
    print("connection to pi1 succesfull")
except:
    print("connection failed")

thread = threading.Thread(target=sendCmds, args=(s,))
thread.start()

#REQUESTS TO CLIENT (CALLED BY WEBSERVER)
#status
def check():
    global running
    takeFlag()
    print("getting status")
    conn.send(GET_STATUS)
    msgLen = int(ord(conn.recv(1).decode(FORMAT)))
    lastSend = (conn.recv(msgLen).decode(FORMAT)) #get time since last message was sent
    status = "Running: True. Time since Last Message:" + lastSend
    if(not running):
        status = "Running: False \t Time since Last Message:" + lastSend
    print(status)
    returnFlag()
    return status #return Status
#exit
def exit(): #send message to Client(PI1) to close
    takeFlag
    conn.send(EXIT)

