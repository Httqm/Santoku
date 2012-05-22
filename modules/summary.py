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


from modules import pattern
from modules import fichier
from modules import config


class Summary(object):
	def __init__(self):
		self.loadFileIni()
		self.loadPattern()


	def loadFileIni(self):
		self.fileIni	= fichier.FileIni({
				'name'	: config.configFilesPath+config.fileSummaryIni,
				'fs'	: '',
				})
		self.fileIniData	= self.fileIni.getData()


	def loadPattern(self):
		try:
			self.summaryPattern=pattern.Pattern({
					'pattern'	: self.fileIniData[config.iniPatternString],
					'variable2tag'	: self.fileIniData[config.iniVarToTagString]
					})
		except KeyError:
			controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" doesn\'t exist in "'+self.fileIni.name+'"' })


	def make(self,params):
		return self.summaryPattern.apply({
				'nbHostsTotal'		: params['total'],
				'nbHostsValid'		: params['valid'],
				'nbHostsIgnored'	: params['ignored']
				})
