#!/usr/bin/python

import struct

class sensorparser:
  def parseTemperatureSensor(self, packet):
    value = struct.unpack("H", packet[2:])[0]
    value = value/2.
  
    if value > 100:
      value = -256.0 + value
   
    return value
  

  def parseSnowDepthSensor(self, packet):
    value = struct.unpack("H", packet[2:])[0]
  
    return value