import sys
from sqlite3 import connect, OperationalError
sys.path.append('config')
from Configuration import *

class MeasurandDAO:

	def __init__(self):
		try:
			self.conn = connect(Configuration.DATABASE_FILE)
		except OperationalError: # Can't locate database file
			exit(1)
		self.cursor = self.conn.cursor()
		
	def persistMeasurand(self, val, unit, locationId, sensorId):
		# persist
		cmd = """INSERT INTO MEASURAND VALUES(null, CURRENT_TIMESTAMP, "%s", "%s", "%s", "%s")""" % (locationId, sensorId, val, unit)
		self.cursor.execute(cmd)

	def insertIntoSyncQueue(self):
		self.cursor.execute('INSERT INTO SYNC_QUEUE (MEASURAND_ID) VALUES (?)', (self.cursor.lastrowid, ))
		
	def closeHandle(self):
		'Closes the connection to the database'
		self.conn.commit() # Make sure all changes are saved
		self.conn.close()
		
		
