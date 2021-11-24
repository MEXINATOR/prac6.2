import sys
import socket
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
print("client starting up...")

#SERVER TO CONNECT WITH
TCP_IP = '192.168.0.124' #'169.254.189.0' 
TCP_PORT = 1234
FORMAT = 'utf-8'    

#SETUP ADC
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0 for LDR
ldr_sensor = AnalogIn(mcp, MCP.P0)
# create an analog input channel on pin 1 for temp sensor
temperature_sensor = AnalogIn(mcp, MCP.P1)

#global var
last_msg_time = (datetime.now()).strftime("%H:%M:%S")

#ACTION FOR EVERY COMMAND
def cmdDo(cmd, s):
    global last_msg_time
    if cmd == 'X':
        print("exiting...")
        s.close()
        quit()
    elif cmd =='S':
        message = last_msg_time #time since last message/sample
        numOfBytes = chr(sys.getsizeof(message)) #number of bytes in the message
        s.send(str(numOfBytes).encode(FORMAT)) #send message length
        s.send(message.encode(FORMAT)) #send message
        print("Status sent")
    elif cmd == 'M':
        last_msg_time = (datetime.now()).strftime("%H:%M:%S")
        temp = round(((temperature_sensor.value - 500)/1000),2)
        message = last_msg_time + "\t"+ str( round(temp,2)) + " C\t\t"  + str(ldr_sensor.value)
        numOfBytes = chr(sys.getsizeof(message)) #number of bytes in the message
        s.send(str(numOfBytes).encode(FORMAT)) #send message length
        s.send(message.encode(FORMAT)) #send message
        print("message sent")
    else:
        print("wrong cmd recieved")
        s.close()
        quit()


#connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#wait to get a command from the server
while True:
    command = s.recv(1).decode(FORMAT)
    cmdDo(command,s)
    


