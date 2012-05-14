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


class AllCommands(object):
	def __init__(self):
		self.output	= ''
		self.commands	= {}
		self.number	= 0


	def add(self,commandData):
		self.commands[commandData['serviceName']]=commandData['serviceCommand']


	def getOutput(self):
		for serviceName in self.commands:
			self.output+=self.commands[serviceName]+"\n"
		return self.output


	def getCount(self):
		return len(self.commands)
