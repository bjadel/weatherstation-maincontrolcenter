#!/usr/bin/python

import optparse
import time
import socket
from MeasurandDAO import *
from QueueSyncer import *
from protocol_backend import *


BUFFER_SIZE = 1024

def persistMeasurand(hostname, portnumber, sensorid, locationid, unit):
	# get value
	val = getValue(hostname, portnumber, sensorid)

	# persist value to db
	persistValue(val, unit, locationid, sensorid)

	# sync the whole queue to mysql server
	syncQueue()

def getValue(hostname, portnumber, sensorid):
	# startup socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((hostname, portnumber))
	
	# let the protocol backend generate our packet
	backend = protocol_backend()
	sock.send(backend.generatePacket(Commands.Sensor_Readout, sensorid))
	   
	# receive the result
	receivedValue = ''
	while (receivedValue == ''):
		receivedValue = sock.recv(BUFFER_SIZE)
	
	# close socket
	sock.close()
		
	# let the backend decode the received value
	value = backend.decodePacket(receivedValue)

	return value
	
def persistValue(value, unit, locationid, sensorid):
	daoMeasurand = MeasurandDAO()
	daoMeasurand.persistMeasurand(value, unit, locationid, sensorid)
	daoMeasurand.insertIntoSyncQueue()
	daoMeasurand.closeHandle()

def syncQueue():
	queueSyncer = QueueSyncer()
	queueSyncer.sync()
	queueSyncer.closeHandle()

parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
parser.add_option("-H", "--host", dest="hostname", default="192.168.0.50", type="string", help="weatherstation lan ip")
parser.add_option("-p", "--port", dest="portnum", default=2069, type="int", help="port number to run from weatherstation")
parser.add_option("-s", "--sensor-id", dest="sensorid", default=1, type="int", help="sensor id")
parser.add_option("-l", "--location-id", dest="locationid", default=1, type="int", help="location id")
parser.add_option("-u", "--unit", dest="unit", default="C", type="string", help="unit")


(options, args) = parser.parse_args()

hostname = options.hostname
portnumber = options.portnum
sensorid = options.sensorid
locationid = options.locationid
unit = options.unit

persistMeasurand(hostname, portnumber, sensorid, locationid, unit)

