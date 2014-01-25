#!/usr/bin/python

from sensorparser import *
import struct

class Sensors:
  Temperature1, Temperature2, Temperature3, Temperature4, SnowDepth = range(1,6)

class commandparser:
  def __init__(self):
    self.sensorparser = sensorparser()
    
  def parseSensorReadout(self, packet):
    sensorID = struct.unpack("B", packet[1:2])[0]
    buf = struct.pack("B", 1)
    
    if sensorID <=4:
      return self.sensorparser.parseTemperatureSensor(packet)
    elif sensorID == 5:
      return self.sensorparser.parseSnowDepthSensor(packet)
    else:
      print "This sensor was not implemented yet!"
      return 0
    
    