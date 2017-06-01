import thread
from serial import Serial
import time

def monitorBatteries():

    serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
    if (serialPort.isOpen() == False):
        serialPort.open()

    outStr = ''
    inStr = ''

    serialPort.flushInput()
    serialPort.flushOutput()

    while True:
        response = serialPort.readline()
        print response
        values = response.split("-----")
        #thread.interrupt_main()

    serialPort.close()



def main():
    thread.start_new_thread(monitorBatteries,())
    print "still in main  "


if __name__ == "__main__":
    main()
