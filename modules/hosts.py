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
from modules import fichier
from modules import pattern
from modules import controller

FileIni		= fichier.FileIni

controller	= controller.Controller()


class AllHosts(object):

	def __init__(self):
		self.loadIniFiles()
		self.loadPatterns()
		self.output=''


	def loadIniFiles(self):
		self.loadIniFile()
		self.loadDirectives()


	def loadIniFile(self):
		fileIniHost	= FileIni({
			'name'	: config.configFilesPath+config.fileHostIni,
			'fs'	: '',
			})
		self.iniFileData	= fileIniHost.getData()
		self.checkIniFile()


	def loadDirectives(self):
		fileIniDirectives	= FileIni({
				'name'		: config.configFilesPath+config.fileDirectivesIni,
				'fs'		: '',
				})
		self.directives	= fileIniDirectives.getData()


	def checkIniFile(self):
		self.searchPatternStanza()
		self.searchVariablesStanza()


	def searchPatternStanza(self):
		try:
			self.iniFileData[config.iniPatternString]
		except KeyError:
			controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+fileIniHost.name})


	def searchVariablesStanza(self):
		try:
			self.iniFileData[config.iniVarToTagString]
		except KeyError:
			controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+fileIniHost.name})


	def loadPatterns(self):
		self.patternHost	= pattern.Pattern({
				'pattern'	: self.iniFileData[config.iniPatternString],
				'variable2tag'	: self.iniFileData[config.iniVarToTagString]
				})

		self.patternDirectives	= pattern.Pattern({
				'pattern'	: self.directives[config.iniPatternString],
				'variable2tag'	: self.directives[config.iniVarToTagString]
				})



class Host(object):
	def __init__(self,params):
		""" Get a CSV line 'hostData' to play with. """
		self.hostData		= params['data']
		self.csvFileName	= params['csvFileName']
		self.controller		= params['controller']
		self.pattern		= {}
		self.allHosts		= params['allHosts']


	def isMarkedToBeIgnored(self):
		return 1 if self.hostData[config.csvHeaderIgnoreHost]=='1' else 0


	def loadDirectives(self):
		try:
			self.hostData[config.csvHostDirectivesNames]
		except KeyError:
			self.controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesNames+'" not found in "'+self.csvFileName+'"'})

		try:
			self.hostData[config.csvHostDirectivesValues]
		except KeyError:
			self.controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesValues+'" not found in "'+self.csvFileName+'"'})

		directives		= ''
		directivesNames		= self.hostData[config.csvHostDirectivesNames].split(config.csvMultiValuedCellFS)
		directivesValues	= self.hostData[config.csvHostDirectivesValues].split(config.csvMultiValuedCellFS)

		for index,value in enumerate(directivesNames):
			directives	+= self.allHosts.patternDirectives.apply({	'directiveName' : directivesNames[index], 'directiveValue' : directivesValues[index]})
		return directives


	def applyHostPattern(self,values):
		return self.allHosts.patternHost.apply(values)


	def loadHostGroupsFromCsv(self):
		return self.hostData[config.csvHeaderHostgroups].split(config.csvMultiValuedCellFS)

