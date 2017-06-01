import thread
##from serial import Serial
from ws4py.client.threadedclient import WebSocketClient
import time
import re
import socket 
import json   
import sys
from time import sleep
from time import gmtime, strftime

CRITICAL_BATTERY_LEVEL              = 3.6
CRITICAL_ULTRASONIC = 15
BROADCAST_NETWORK                   = '192.168.8.255'
WEBSOCKET_SERVER_ENDPOINT           = "ws://localhost:8080/Coordinator/coordinator"

AGENT_IP                            = ""
COORDINATOR                         = ""

AREA_MAP                            = []
INTITAL_PLACE                       = []

currentEvent                        = ""
incomeMsg                           = ""
assignedArea                        = []

class Priority:
    LOW                             = 0
    NORMAL                          = 1
    HIGH                            = 2


##-------------------- List of Intrrupts ---------------------------##

class Interrupt:
    NO_EVENT                        = 0
    INCOMING_MESSAGE                = 1    
    CRITICAL_BATTERY_LEVEL_REACHED  = 2
    REGISTER_TO_SERVICE             = 3
    
    



##-------------------- List of Intrrupts ---------------------------##
class Message:
    READY_TO_WORK                   = 0
    KEY_PLACE_AREAS                 = 1    
    LIST_OF_OTHER_AGENTS            = 2
    LOCATION_MAP                    = 3
    ASSIGNED_AREA                   = 4
    PERSONS_DETAILS                 = 5
    SUSPICIOUS_PERSON               = 6
    CURRENT_BATTERY_VOLTAGE         = 7
    CRITICAL_BATTERY_LEVEL          = 8
    PERSON_DETECTED                 = 9
    CURRENT_LOCATION                = 10


##-------------------- Battery Monitoring Service ---------------------------##



def monitorBatteries():

##    serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
##    if (serialPort.isOpen() == False):
##        serialPort.open()
##
##    outStr = ''
##    inStr = ''
##
##    serialPort.flushInput()
##    serialPort.flushOutput()

    while True:
##        response = serialPort.readline()
        response = "3.81-----3.61"
        status = False
##        print response

        values = response.split("-----")
        for value in values :
            value = float(re.findall("\d+\.\d+", value)[0])
            if value < float(CRITICAL_BATTERY_LEVEL):
                status = True
            else:
                status = False
        if status == True:             
            thread.interrupt_main()
            print "Critical Battery Level"
            break
#    serialPort.close()

##-------------------- End of Battery Monitoring Service---------------------------##

##-------------------- Start of Ultrasonic Method---------------------------------##
def ultrasonicDistance():
    print "-----ultrasonicDistance-----"
    while True:
        ##        response = serialPort.readline()

        # //////call ULTRASONIC method here **********************************************************
        response = 20
        status = False
        # print response
        if response < float(CRITICAL_ULTRASONIC):
            status = True
        else:
            status = False
        if status == True:
            # thread.interrupt_main()


            # //////call Obstacle avoidance here **********************************************************
            # check current location
            # reconfiguration of the path
            print "Obstacle Detected"
            break

##-------------------- End of Ultrasonic Method---------------------------------##

def serverNavigation_IP():
    from random import randint
    while True:
        number= (randint(0,100))
        time.sleep(0.1)
        status = False
        print "Random:", number
        if number == 10 or number == 2: # found
            print "Stsop"
            status= True
            thread.interrupt_main()
            # from TurtleGUI_TSP import stopAgent as stopAgent
            # stopAgent()

            break
        else:
            status= False
            # print "Not Found"

##-------------------- Register to the Service via Coordinator---------------------##
def registerToService ():    
    addr = (BROADCAST_NETWORK, 33333) # broadcast address explicitly

    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket

    print "Starting the registering process"

    data1 = "register"
    # Almost infinite loop... ;)
    while True:    
        if UDPSock.sendto(data1, addr):
                print "Sending message '%s'..." % data1                
                try:
                        UDPSock.settimeout(5)
                        data, addr = UDPSock.recvfrom(1024)
                        UDPSock.close()
                        print "Server IP is %s" %(data)
                        data1 = []
                        data1.append(data)
                        data1.append(addr[0])
                        UDPSock.close()
                        
                        break
                except:
                        print "Time out exception"




    UDPSock.close()             # Close socket
    print 'Client stopped.'
    return data1;
##-------------------- End of Register to the Service ------------------------------##



##-------------------- WebSocket Connection ----------------------------------------##

class DummyClient(WebSocketClient):
    def opened(self): 
        print "Connection Established"
        
    def closed(self, code, reason=None):
        print "Connection Closed down", code, reason        

    def received_message(self, m):
        global incomeMsg
        incomeMsg = str(m)        
        global currentEvent
        currentEvent = Interrupt.INCOMING_MESSAGE
        thread.interrupt_main()

##-------------------- Draw obstacles ---------------------------------------------##

def drawObstacles(rectangle):
    global AREA_MAP
    for y in range(int(rectangle[1]), int(rectangle[1])+int(rectangle[3])+1):
        for x in range(int(rectangle[0]), int(rectangle[0])+int(rectangle[2])+1):
            if x == rectangle[0] or x == rectangle[0] + rectangle[2] or y == rectangle[1] or y == rectangle[1] + rectangle[3]:
                AREA_MAP[y][x] = 1

##    for x in range(0, len(AREA_MAP)):        
##        print AREA_MAP[x]
## 
        
            

##-------------------- Agent Main Process ------------------------------------------##   
def agentMainProcess(currentEvent,group):
    if(currentEvent != Interrupt.NO_EVENT ):
        if(currentEvent == Interrupt.REGISTER_TO_SERVICE):
            ws = group.get(COORDINATOR,None);
            msg = formatTheMessageAndSend(Message.READY_TO_WORK,Message.READY_TO_WORK,AGENT_IP,COORDINATOR,Priority.NORMAL);            
            ws.send(msg)
        elif(currentEvent == Interrupt.INCOMING_MESSAGE):
           
            j = json.loads(incomeMsg)
            tag = j['Header'][0]['Tag'][0]
            if(int(tag) == int(Message.LIST_OF_OTHER_AGENTS)):
                agentList = j['Body'][0]['Message'][0]
                print agentList

                ##########################################################################################Create Agent Network#############################
                ws = group.get(COORDINATOR,None);
                msg = formatTheMessageAndSend(Message.LOCATION_MAP,Message.LOCATION_MAP ,AGENT_IP,COORDINATOR,Priority.NORMAL);            
                ws.send(msg)
            elif(int(tag) == int(Message.LOCATION_MAP)):                
##                map = j['Body'][0]['Message'][0]
                map = '{"height":10,"width":15,"data1":[[5,5,8,3],[2,2,7,6]],"data2":[[3,3],[6,6]],"data3":[3,3]}'
                j = json.loads(map)
                global AREA_MAP
                height =  int(j['height'])
                width  =  int(j['width'])
                for x in range(0, height):
                    row = []
                    for y in range(0, width):
                        row.append(0)
                    AREA_MAP.append(row)

                for x in range(0, len(j['data1'])):
                    drawObstacles(j['data1'][x])

                for x in range(0, len(j['data2'])):
                    AREA_MAP[j['data2'][x][1]][j['data2'][x][0]] = 2


                global INTITAL_PLACE
                INTITAL_PLACE = j['data3']
                
                print "Map is ready"
                ws = group.get(COORDINATOR,None);
                msg = formatTheMessageAndSend(Message.ASSIGNED_AREA,Message.ASSIGNED_AREA,AGENT_IP,COORDINATOR,Priority.NORMAL);            
                ws.send(msg)
                for x in range(0, len(AREA_MAP)):
                  print AREA_MAP[x]
                
            elif(int(tag) == int(Message.ASSIGNED_AREA)):
                global assignedArea
                assignedArea = j['Body'][0]['Message'][0]
                print "Area assigned"
                print assignedArea

            ############################## initializing completed ##################################################################
            elif(int(tag) == int(Message.PERSONS_DETAILS)):
                f_degree=1
                b_degree=2
                r_degree=3
                l_degree=4
                ######### Getting key points path #############


                from TSP import main as main_from_TSP
                main_from_TSP(AREA_MAP, f_degree, b_degree, r_degree, l_degree, assignedArea)
                ######### End of getting key points path #############
                             

##-------------------- Message Format ------------------------------------------##   
def formatTheMessageAndSend(msg, tag, sender, receiver,priority):
    
    message =   {   'Header'  : 
                            {
                             'Sender'              : sender, 
                             'Reciever'            : receiver,
                             'TimeStamp'           : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                             'Tag'                 : tag,
                             'Priority'            : priority,
                             'CoomunicatorGroup'   : "",
                            },
                    'Body'    :
                            {
                             'Message'              : msg                             
                             }
                }
    
    msgPacket = json.dumps(message)    
    return msgPacket


##-------------------- End of WebSocket Connection ---------------------------------##



def main():
    try:
        global currentEvent
        currentEvent = Interrupt.NO_EVENT
        CommunicatorGroup = {}

        ######### Start Battery Monitoring Thread #####
        thread.start_new_thread(monitorBatteries,())

        
        ######### Register to the Service #############
        serverIp    = registerToService()
        global COORDINATOR
        COORDINATOR = serverIp[0]
        global AGENT_IP
        AGENT_IP    = serverIp[1]
        newEndPoint = "ws://"+COORDINATOR+":"+WEBSOCKET_SERVER_ENDPOINT.split(":")[2]
       
        ######### Create Web Socket Connection ########
        
        ws = DummyClient(newEndPoint)
        ws.connect()
     
        CommunicatorGroup[COORDINATOR] = ws
        currentEvent = Interrupt.REGISTER_TO_SERVICE
         
        ######### Start the main process of Agent #######
        while True:          
            try:
                agentMainProcess(currentEvent,CommunicatorGroup);
                currentEvent = Interrupt.NO_EVENT
                ws.run_forever()
            except KeyboardInterrupt:
                print('interrupted')        
    
    except KeyboardInterrupt:
       print "Exception"
       ws.close()

    print "App closed"

        
if __name__ == "__main__":
    main()
