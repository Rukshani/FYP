import time
import smbus
import RPi.GPIO as IO
import sys
import Tkinter as tk
import os
import smbus
import time
import math
import thread

IO.setwarnings(False)
IO.setmode (IO.BOARD)

IO.setup(31,IO.OUT)
IO.setup(33,IO.OUT)
IO.setup(35,IO.OUT)
IO.setup(37,IO.OUT)
IO.setup(38,IO.OUT)
IO.setup(40,IO.OUT)

left    = IO.PWM(38,100)
right   = IO.PWM(40,100)

left.start(0)
right.start(0)

DONE=""
RANGE=5

class Compass:
  bus = smbus.SMBus(1)
  address = 0x1e

  def __init__(self, address):
    self.address = address

  def read_byte(self, adr):
    return self.bus.read_byte_data(self.address, adr)

  def read_word(self, adr):
    high = self.bus.read_byte_data(self.address, adr)
    low = self.bus.read_byte_data(self.address, adr+1)
    val = (high << 8) + low
    return val

  def read_word_2c(self, adr):
    val = self.read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

  def write_byte(self, adr, value):
    self.bus.write_byte_data(self.address, adr, value)

  def getOrientation(self):
    self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
    self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    self.write_byte(2, 0b00000000) # Continuous sampling

##    time.sleep(3)
    scale = 0.92

    x_offset = 46
    y_offset = -117
    x_out = (self.read_word_2c(3) - x_offset) * scale
    y_out = (self.read_word_2c(7) - y_offset) * scale
    z_out = (self.read_word_2c(5)) * scale

    bearing  = math.atan2(y_out, x_out)
    if (bearing < 0):
      bearing += 2 * math.pi

    return math.degrees(bearing)

class Motion:
  global tickDirection
  tickDirection=[]
  def forward(self,actualDir):
    print "working forward........................................."
    IO.output(31,IO.HIGH)
    IO.output(33,IO.LOW)
    IO.output(35,IO.LOW)
    IO.output(37,IO.HIGH)

    left.ChangeDutyCycle(60)
    right.ChangeDutyCycle(60)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)

    tickDirection.append(actualDir)
    print "------------------------------------------------------"
    print tickDirection
    print "Forward"

  def right(self):
    print "working right........................................."
    IO.output(31,IO.HIGH)
    IO.output(33,IO.LOW)
    IO.output(35,IO.HIGH)
    IO.output(37,IO.LOW)

    left.ChangeDutyCycle(30)
    right.ChangeDutyCycle(30)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print "Right"

  def left(self):
    print "working left........................................."
    IO.output(31,IO.LOW)
    IO.output(33,IO.HIGH)
    IO.output(35,IO.LOW)
    IO.output(37,IO.HIGH)

    left.ChangeDutyCycle(30)
    right.ChangeDutyCycle(30)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print "Left"


def calDir(target, current, compassRange=RANGE):
  motion=Motion()
  target=target%360
  current=current%360
  delta=(target-current)%360
  print("Target=%f Current=%f Delta=%f"%(target,current,delta))

  if delta <= compassRange:
    status=DONE
  else:
    if delta>180:
      status=motion.left()
    else:
      status=motion.right()
  return status

def main():
  motion=Motion()
  compass = Compass(0x1e)
  while(True):
    ANGLE=287
    try:
      angleTarget=float(ANGLE)
      status=motion.left()
      while (status!=DONE):
        currentAngle=compass.getOrientation()
        status=calDir(angleTarget,currentAngle)
        time.sleep(1)
      print("Angle Reached!")
      break
    except ValueError:
      print("Enter valid angle!")
      pass

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print ("Finish")
