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


from modules import config


class Controller(object):
	def __init__(self):
		self.mySys = __import__('sys')


	def die(self,params):
		""" Display an error message and leave the program. """
		print params['exitMessage']
		print config.messageDie
		self.mySys.exit(2)


	def showDebug(self,message):
		if config.debug:
			import inspect
			print "\n" \
			    + " ++=================== DEBUG =========================\n" \
			    + ' || FILE    : ' + str(inspect.stack()[1][1]) + "\n" \
			    + ' || LINE    : ' + str(inspect.stack()[1][2]) + "\n" \
			    + ' || CALLER  : ' + str(inspect.stack()[1][3]) + "\n" \
			    + ' || MESSAGE : ' + str(message) + "\n" \
			    + " ++================== /DEBUG =========================\n" \


	def checkConfigValues(self):
		self.checkCsvFieldAndListSeparatorsAreDifferent()


	def checkCsvFieldAndListSeparatorsAreDifferent(self):
		if config.csvFileFs == config.csvFileParamFs:
			self.die({'exitMessage':'The values for the CSV field separator and the CSV list separator must be different in ' + config.configFile})

