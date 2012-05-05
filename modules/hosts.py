#!/usr/bin/env python

# Copyright (C) 2012 Matthieu FOURNET, fournet.matthieu@gmail.com
#
# This file is part of Santoku.
#
# Santoku is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Santoku is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Santoku.  If not, see <http://www.gnu.org/licenses/>
#


"""
http://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
"""

########################################## ##########################################################
# 
########################################## ##########################################################
class Host(object):	# 'object' : ancestor of all classes
	def __init__(self,hostData):
		""" Get a CSV line 'hostData' to play with. """
		self.hostData=hostData


	def loadHostGroups(self):
		"""
		Read 'hostgroups' column from CSV, and split it by its field separator '|'
		Return O on success, >0 on failure
		"""
		hostGroupsList=self.hostData['hostgroups'].split('|')

		self.hostGroupsList=hostGroupsList
		return 0


	def getHostGroups(self):
		""" Load + return hostgroup list """
		result=self.loadHostGroups()
		if(result):
			import sys
			sys.exit(1)	# http://docs.python.org/library/sys.html?highlight=sys.exit#sys.exit
		else:
			return self.hostGroupsList

