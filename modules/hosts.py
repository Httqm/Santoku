#!/usr/bin/python

"""
http://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
"""

########################################## ##########################################################
# 
########################################## ##########################################################
class Host(object):	# 'object' : ancestor of all classes
	def __init__(self,hostData):
		""" Get a CSV line 'hostData' to play with. """
#		print hostData
		self.hostData=hostData
#		print 'HOSTNAME : '+self.hostData['host_name']


	def loadHostGroups(self):
		"""
		Read 'hostgroups' column from CSV, and split it by its field separator '|'
		Return O on success, >0 on failure
		"""
		hostGroupsList=self.hostData['hostgroups'].split('|')
#		print 'HOSTGROUPS : '+hostGroupsList

#ligne.split(self.fs)

		self.hostGroupsList=hostGroupsList
		return 0


	def getHostGroups(self):
		""" Load + return hostgroup list """
		result=self.loadHostGroups()
		if(result):
#			print str(result)
			import sys
			sys.exit(1)	# http://docs.python.org/library/sys.html?highlight=sys.exit#sys.exit
		else:
			return self.hostGroupsList

