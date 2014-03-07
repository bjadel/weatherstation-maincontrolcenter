import sys, json
from sqlite3 import connect, OperationalError
sys.path.append('/home/pi/station/weatherstation-maincontrolcenter/programs/config')
from Configuration import *
from MeasurandWebservice import *

class QueueSyncer:

	def __init__(self):
		# sqlite connecton
		try:
			self.conn = connect(Configuration.DATABASE_FILE)
			self.cursor = self.conn.cursor()
		except OperationalError: # Can't locate database file
			exit(1)
				
	def sync(self):
		data = self.getData()
		json_data = json.dumps(data)
		webService = MeasurandWebservice()
		success = webService.sync(json_data)
		if (success):
			# remove 
			self.clearSyncQueue()

	def closeHandle(self):
		'Closes the connection to the database'
		self.conn.commit() # Make sure all changes are saved
		self.conn.close()

	def getData(self):
		cmd = "SELECT M.CREATIONDATE, M.LOCATION_ID, M.SENSOR_ID, M.VALUE, M.UNIT FROM MEASURAND M INNER JOIN SYNC_QUEUE S ON M.ID = S.MEASURAND_ID"
		self.cursor.execute(cmd)
		return self.cursor.fetchall()

	def clearSyncQueue(self):
		cmd = "DELETE FROM SYNC_QUEUE"
		self.cursor.execute(cmd)
