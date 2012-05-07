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


class Service2(object):
	def __init__(self,params):
		self.currentCsvLine	= params['currentCsvLine']
		self.csvServiceName	= params['serviceCsvName']
		self.cleanName		= self.csvServiceName.replace(config.csvHeaderFs+config.csvHeaderDo,'')

		self.loadDirectivesIni()
		self.patternDirectives	= pattern.Pattern({
			'pattern'	: self.cfgHostDirectives[config.iniPatternString],
			'variable2tag'	: self.cfgHostDirectives[config.iniVarToTagString]
		})


	def loadDirectivesIni(self):

		"""
		objHostServiceDirectivesFileIni	= FileIni({
			'name'		: config.configFilesPath+config.fileDirectivesIni,
			'fs'		: '',
			'controller'	: controller
			})
		cfgHostDirectives		= objHostServiceDirectivesFileIni.getData()
		"""
		fileDirectivesIni	= fichier.FileIni({
			'name'		: config.configFilesPath+config.fileDirectivesIni,
			'fs'		: ''
			})
		self.cfgHostDirectives		= fileDirectivesIni.getData()


	def isEnabled(self):
		return 1 if self.currentCsvLine[self.csvServiceName]=='1' else 0


	def getName(self):
		return self.cleanName


	def hasDirectives(self,sourceCsvFile):
		hasDirectives	= 1

		for columnName in [self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesNames, self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesValues]:

			if(sourceCsvFile.columnExists(columnName)):
				hasDirectives	= hasDirectives and self.currentCsvLine[columnName]
			else:
				hasDirectives	= 0

		return hasDirectives


	def loadDirectivesFromCsvData(self):
		"""
		directivesNames	= csvData[hostName][serviceName+config.csvHeaderFs+config.csvServiceDirectivesNames].split(config.csvMultiValuedCellFS)
		directivesValues= csvData[hostName][serviceName+config.csvHeaderFs+config.csvServiceDirectivesValues].split(config.csvMultiValuedCellFS)
		"""
		self.directives={
			'names'		: self.currentCsvLine[self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesNames].split(config.csvMultiValuedCellFS),
			'values'	: self.currentCsvLine[self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesValues].split(config.csvMultiValuedCellFS)		
			}



	def applyServiceDirectivesPattern(self):
		"""
		serviceDirectives	= ''

		for name,value in enumerate(directivesNames):
			serviceDirectives+=objPatternDirectives.apply({
				'directiveName'		: directivesNames[name],
				'directiveValue'	: directivesValues[name]
				})
		"""

		self.serviceDirectives	= ''
		for name,value in enumerate(self.directives['names']):
			#self.serviceDirectives+=objPatternDirectives.apply({
			self.serviceDirectives+=self.patternDirectives.apply({
				'directiveName'		: self.directives['names'][name],
				'directiveValue'	: self.directives['values'][name]
				})


		return self.serviceDirectives










class Service(object):
	def __init__(self,params):
		self.params	= params
		self.cleanName	= self.params['name'].replace(config.csvHeaderFs+config.csvHeaderDo,'')	# cleanName = name without ':do'


	def getName(self):
		return self.cleanName


	def loadServiceData(self):
		"""
		For the current host and the current service, return : 
		- 'clean' CSV header lines (without the 'serviceName:')
		- cell values (including multiple values and field separators if any)
		"""
		import re
		serviceCsvData={} # temporary dict

		# storing CSV data in a dict to play with it later
		for field in self.params['csvHeader']:
			match=re.search(self.cleanName+config.csvHeaderFs+'.*', field)
			if(match):
				# parsing all CSV columns related to this service
				serviceCsvData[field.replace(self.cleanName+config.csvHeaderFs,'')]=self.params['csvDataLine'][field]

		# appending 'serviceDirectives'
		# serviceCsvData contains 2 useless keys : 'serviceDirectivesNames' and 'serviceDirectivesValues'
		serviceCsvData['serviceDirectives']=self.params['serviceDirectives']

		return serviceCsvData


	def buildArrayOfServices(self):
		"""
		Return an associative array containing all service(s) data ready to be injected into pattern.
		This method handle multi-valued CSV cells
		"""
		serviceCsvData	= self.loadServiceData()
		champsValeurs	= {}

		# Parsing data stored in dict to register as many services as the number of values in mutli-valued cells
		maxRounds	= 1
		currentRound	= 0

		while currentRound < maxRounds:
			champsValeurs[currentRound]	= {
				config.csvHeaderHostName	: self.params['hostName'],
				config.csvHeaderUse		: config.csvGenericService
				}
			for serviceField in serviceCsvData:
				valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(self.params['fieldSeparator'])

				# Excluding the service directives columns here to avoid duplicating the service definition
				if((serviceField != config.csvServiceDirectivesNames) and (serviceField != config.csvServiceDirectivesValues)):
					maxRounds	= len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds

				try:
					tmpValue	= valuesOfMultiValuedCell[currentRound]
				except IndexError:
					tmpValue	= valuesOfMultiValuedCell[0]

				champsValeurs[currentRound][serviceField]=tmpValue

			currentRound+=1

		return { 'champsValeurs' : champsValeurs, 'maxRounds' : maxRounds }
