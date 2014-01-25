#!/usr/bin/python

from commandparser import *
import struct

class Commands:
  Sensor_Readout, Reset = [1,255]

class protocol_backend:
  def __init__(self):
    self.commandparser = commandparser()
  
  def generatePacket(self, CommandID, SensorID):
    buf = struct.pack("B", CommandID)
    buf = buf + struct.pack("B", SensorID)

    return buf
  
  
  def decodePacket(self,packet):
    commandID = struct.unpack("B", packet[0:1])[0]
  
    if commandID == Commands.Sensor_Readout:
      # we received a temperature measurement
      return self.commandparser.parseSensorReadout(packet)
    elif commandID == Commands.Reset:
      return 0
    else:
      print "This command has not been implemented yet"
    return 0