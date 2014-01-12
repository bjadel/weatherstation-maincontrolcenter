import sqlite3

class MeasurandDAO:

	DATABASE_FILE = '/mnt/data/database/weatherstation/sqlite/var/measuranddb'

	def __init__(self):
		try:
			self.conn = sqlite3.connect(MeasurandDAO.DATABASE_FILE)
		except sqlite3.OperationalError: # Can't locate database file
			exit(1)
		self.cursor = self.conn.cursor()
		
	def persistMeasurand(self, val, unit, locationId, sensorId):
		# persist
		cmd = """INSERT INTO measurand VALUES(null, CURRENT_TIMESTAMP, "%s", "%s", "%s", "%s")""" % (locationId, sensorId, val, unit)
		self.cursor.execute(cmd)
		
	def closeHandle(self):
		'Closes the connection to the database'
		self.conn.commit() # Make sure all changes are saved
		self.conn.close()
		
		
