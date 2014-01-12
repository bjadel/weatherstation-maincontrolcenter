#!/mnt/opt/usr/bin/python

import optparse
import time
import struct
import socket
import MeasurandDAO

BUFFER_SIZE = 1024

def persistMeasurand(hostname, portnumber, sensorid, locationid, unit):
	# get value
	val = getValue(hostname, portnumber, sensorid)
	
	# persist value to db
	persistValue(val, unit, locationid, sensorid)

def getValue(hostname, portnumber, sensorid):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((hostname, portnumber))
	
	sock.send(struct.pack("B", sensorid))
	receivedValue = ''
	while (receivedValue == ''):
		receivedValue = sock.recv(BUFFER_SIZE)
	
	# close socket
	sock.close()
		
	value = struct.unpack("H", receivedValue[1:])[0]
	value = value/2.
	if value > 100:
		value = -256.0 + value
	
	return value
	
def persistValue(value, unit, locationid, sensorid):
	
	print value
	
	daoMeasurand = MeasurandDAO.MeasurandDAO()
	daoMeasurand.persistMeasurand(value, unit, locationid, sensorid)
	daoMeasurand.closeHandle()

parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
parser.add_option("-H", "--host", dest="hostname", default="77.64.132.34", type="string", help="weatherstation lan ip")
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

