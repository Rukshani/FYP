# import RPi.GPIO as IO
import time
import sys
import Tkinter as tk
import os
import thread

# IO.setwarnings(False)
# IO.setmode(IO.BOARD)
#
# IO.setup(31,IO.OUT)
# IO.setup(33,IO.OUT)
# IO.setup(35,IO.OUT)
# IO.setup(37,IO.OUT)
# IO.setup(38,IO.OUT)
# IO.setup(40,IO.OUT)
#
# left    = IO.PWM(38,100)
# right   = IO.PWM(40,100)

# left.start(0)
# right.start(0)

servo_range = [2, 3, 4, 5, 6, 7, 8]

##path = ['^', 'v', '>', '<']
tdelay = 80
global coveredLocationList
coveredLocationList = []  # edit 7


def forward():
    # IO.output(31,IO.HIGH)
    # IO.output(33,IO.LOW)
    # IO.output(35,IO.LOW)
    # IO.output(37,IO.HIGH)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Forward")


def right():
    # IO.output(31,IO.HIGH)
    # IO.output(33,IO.LOW)
    # IO.output(35,IO.HIGH)
    # IO.output(37,IO.LOW)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Right")


def left():
    # IO.output(31,IO.LOW)
    # IO.output(33,IO.HIGH)
    # IO.output(35,IO.LOW)
    # IO.output(37,IO.HIGH)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Left")


def key_input(path, f_degree, b_degree, r_degree, l_degree, initialPoint, currentLocationList):  # edit 5
    ##    key_press = event.keysym.lower()
    ##    print (key_press)
    print "pathcounterpathcounterpathcounterpathcounter", initialPoint

    key_press_index = 0

    for key_press in path:
        # print "Current locations", currentLocationList[key_press_index] # edit 6
        coveredLocationList.append(currentLocationList[key_press_index])
        # time.sleep(0.1)
        # print "coveredLocationList: ", coveredLocationList
        key_press_index = key_press_index + 1

def stop(currentLocation,speedGlobal, gridGlobal, f_degreeGlobal, b_degreeGlobal, r_degreeGlobal, l_degreeGlobal,initalLocation):
    print "Reaching Initallllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll"
    print "currentLocationcompassControl",currentLocation
    print "FirstLocationcompassControl",initalLocation

    #---------------------send this location to cordinator-----------------------------------********************************

    #-------------------returning to initial location
    from TurtleGUI_TSP import search as search
    search(currentLocation,initalLocation,speedGlobal,gridGlobal,f_degreeGlobal,b_degreeGlobal,r_degreeGlobal,l_degreeGlobal,initalLocation)


##command = tk.Tk()
##command.bind_all('<Key>', key_input)
##command.mainloop()

##key_input(path)
