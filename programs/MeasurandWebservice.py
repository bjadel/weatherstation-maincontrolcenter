import sys
import urllib
import urllib2
sys.path.append('config')
from Configuration import *

class MeasurandWebservice:	

	def sync(self, data):
		try:
			passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
			passman.add_password(None, Configuration.WEBSERVICE_SYNC_URL, Configuration.WEBSERVICE_BASIC_AUTH_USERNAME, Configuration.WEBSERVICE_BASIC_AUTH_PW)
			authhandler = urllib2.HTTPBasicAuthHandler(passman)
			opener = urllib2.build_opener(authhandler)
			urllib2.install_opener(opener)

			params= { "version" : "0.1",
			          "format" : "json",
			          "measurands" : data }

			jsonResults = urllib2.urlopen(Configuration.WEBSERVICE_SYNC_URL, urllib.urlencode(params)).read()
			print jsonResults
		except Exception, e:
			print e
			return False
		return True
		
