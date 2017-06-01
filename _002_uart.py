from serial import Serial
import time

serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
if (serialPort.isOpen() == False):
    serialPort.open()

outStr = ''
inStr = ''

serialPort.flushInput()
serialPort.flushOutput()

print "ready for serial"

##for i, a in enumerate(range(33, 126)):
##    outStr += chr(a)
##
##    serialPort.write(outStr)
##    time.sleep(0.05)
##    inStr = serialPort.read(serialPort.inWaiting())
##
##    print "inStr =  " + inStr
##    print "outStr = " + outStr
##
##    if(inStr == outStr):
##        print "WORKED! for length of %d" % (i+1)
##    else:
##        print "failed"

while True:
    serialPort.write("start")
    response = serialPort.readline()
    print response

serialPort.close()
