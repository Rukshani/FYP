from __future__ import division
# import RPi.GPIO as GPIO
from time import sleep
import math

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(11, GPIO.IN)
# GPIO.setup(12, GPIO.IN)

countRisLeft=0
countFallLeft=0
countRisRight=0
countFallRight=0

def my_callback():
    global countRisLeft
    global countFallLeft
    global countRisRight
    global countFallRight

    # if GPIO.input(11):
    countRisRight=countRisRight+1
    print "Rising edge detected on 11"
    return countRisRight

    # else:
    #     countFallRight=countFallRight+1
    #     print "Falling edge detected on 11"
    #     return countFallRight
    #
    # if GPIO.input(12):
    #     countRisLeft=countRisLeft+1
    #     print "Rising edge detected on 12"
    #
    # else:
    #     countFallLeft=countFallLeft+1
    #     print "Falling edge detected on 12"

# GPIO.add_event_detect(11, GPIO.BOTH, callback=my_callback)
# GPIO.add_event_detect(12, GPIO.BOTH, callback=my_callback)

my_callback()

distanceForATick=2*math.pi*3.35/20
print "distanceForATick: ",distanceForATick

try:
    sleep(1)
    # print "RisingLeft",countRisLeft
    # print "FallingLeft", countFallLeft
    # TotalDistanceFromLeft=distanceForATick*max(countRisLeft,countFallLeft)
    # print "TotalDistanceFromLeft:", TotalDistanceFromLeft

    print "RisingRight",countRisRight
    print "FallingRight", countFallRight
    TotalDistanceFromRight=distanceForATick*max(countRisRight,countFallRight)
    print "TotalDistanceFromRight:", TotalDistanceFromRight

finally:
    # GPIO.cleanup()
    print "Finish"
