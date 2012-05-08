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
import re

Pattern	= pattern.Pattern
FileIni	= fichier.FileIni

class AllServices(object):

	def __init__(self):
		self.output=''


	def getList(self,csvHeaders):
		self.list=[]
		for field in csvHeaders:
			match=re.search('.*'+config.csvHeaderFs+config.csvHeaderDo+'$', field)
			if(match):
				self.list.append(field)

		return self.list




class Service2(object):
	def __init__(self,params):
		self.currentCsvLine	= params['currentCsvLine']
		self.csvServiceName	= params['serviceCsvName']
		self.cleanName		= self.csvServiceName.replace(config.csvHeaderFs+config.csvHeaderDo,'')

		self.loadIniFiles()
		self.loadPatterns()



	def loadIniFiles(self):
		self.loadIniFile()
		self.loadDirectivesIni()


	def loadIniFile(self):
		"""
			# Load service data from './config/"serviceName".ini'
			objServiceFileIni	= FileIni({
					'name'		: config.configFilesPath+service.getName()+'.ini',
					'fs'		: '',
					})

			# Load INI file data
			cfgDataService		= objServiceFileIni.getData()
		"""
		fileIni	= FileIni({
			'name'	: config.configFilesPath+self.cleanName+'.ini',
			'fs'	: '',
			})
		self.fileIniData	= fileIni.getData()
		self.checkFileIni()



	def checkFileIni(self):
		"""
			try:
				cfgDataService[config.iniPatternString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+objServiceFileIni.name})

			try:
				cfgDataService[config.iniVarToTagString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+objServiceFileIni.name})
		"""
		try:
			self.fileIniData[config.iniPatternString]
		except KeyError:
			controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+fileIni.name})

		try:
			self.fileIniData[config.iniVarToTagString]
		except KeyError:
			controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+fileIni.name})


	def loadPatterns(self):
		"""
		def loadPatterns(self):
			self.patternHost	= pattern.Pattern({
					'pattern'	: self.iniFileData[config.iniPatternString],
					'variable2tag'	: self.iniFileData[config.iniVarToTagString]
					})

			self.patternDirectives	= pattern.Pattern({
					'pattern'	: self.directives[config.iniPatternString],
					'variable2tag'	: self.directives[config.iniVarToTagString]
					})

		objPatternService	= Pattern({
				'pattern' : cfgDataService[config.iniPatternString],
				'variable2tag' : cfgDataService[config.iniVarToTagString]
				})
		"""
		self.patternService	= Pattern({
			'pattern'	: self.fileIniData[config.iniPatternString],
			'variable2tag'	: self.fileIniData[config.iniVarToTagString]
			})
		self.patternDirectives	= Pattern({
			'pattern'	: self.cfgHostDirectives[config.iniPatternString],
			'variable2tag'	: self.cfgHostDirectives[config.iniVarToTagString]
			})


	def loadDirectivesIni(self):
		fileDirectivesIni	= FileIni({
			'name'		: config.configFilesPath+config.fileDirectivesIni,
			'fs'		: ''
			})
		self.cfgHostDirectives	= fileDirectivesIni.getData()


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
		self.directives	= {
			'names'		: self.currentCsvLine[self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesNames].split(config.csvMultiValuedCellFS),
			'values'	: self.currentCsvLine[self.cleanName+config.csvHeaderFs+config.csvServiceDirectivesValues].split(config.csvMultiValuedCellFS)		
			}



	def applyServiceDirectivesPattern(self):
		self.serviceDirectives	= ''
		for name,value in enumerate(self.directives['names']):
			self.serviceDirectives+=self.patternDirectives.apply({
				'directiveName'		: self.directives['names'][name],
				'directiveValue'	: self.directives['values'][name]
				})
		return self.serviceDirectives



	def buildArrayOfServices(self,params):
		"""
		Return an associative array containing all service(s) data ready to be injected into pattern.
		This method handle multi-valued CSV cells
		"""
		serviceCsvData	= self.loadServiceData(params)
		champsValeurs	= {}

		# Parsing data stored in dict to register as many services as the number of values in mutli-valued cells
		maxRounds	= 1
		currentRound	= 0

		while currentRound < maxRounds:
			champsValeurs[currentRound]	= {
				config.csvHeaderHostName	: params['hostName'],
				config.csvHeaderUse		: config.csvGenericService
				}
			for serviceField in serviceCsvData:
#				valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(params['fieldSeparator'])
				valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(config.csvMultiValuedCellFS)

				# Excluding the service directives columns here to avoid duplicating the service definition
				if((serviceField != config.csvServiceDirectivesNames) and (serviceField != config.csvServiceDirectivesValues)):
					maxRounds	= len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds

				try:
					tmpValue	= valuesOfMultiValuedCell[currentRound]
				except IndexError:
					tmpValue	= valuesOfMultiValuedCell[0]

				champsValeurs[currentRound][serviceField]=tmpValue

			currentRound+=1
		
		self.result=	{ 'champsValeurs' : champsValeurs, 'maxRounds' : maxRounds }
		return self.result


	def loadServiceData(self,params):
		"""
		For the current host and the current service, return : 
		- 'clean' CSV header lines (without the 'serviceName:')
		- cell values (including multiple values and field separators if any)
		"""
		import re
		serviceCsvData={} # temporary dict

		# storing CSV data in a dict to play with it later
#		for field in self.params['csvHeader']:
		for field in params['csvHeader']:
			match=re.search(self.cleanName+config.csvHeaderFs+'.*', field)
			if(match):
				# parsing all CSV columns related to this service
#				serviceCsvData[field.replace(self.cleanName+config.csvHeaderFs,'')]=self.params['csvDataLine'][field]
				serviceCsvData[field.replace(self.cleanName+config.csvHeaderFs,'')]=params['csvDataLine'][field]

		# appending 'serviceDirectives'
		# serviceCsvData contains 2 useless keys : 'serviceDirectivesNames' and 'serviceDirectivesValues'
		serviceCsvData['serviceDirectives']=params['serviceDirectives']

		return serviceCsvData


	def make(self):
		"""
			# finally apply service pattern as many time as the maximum number of values in multi-valued CSV cells
			for i in xrange(result['maxRounds']):
				allServices.output+=objPatternService.apply(result['champsValeurs'][i])
		"""
		bla=''
		for i in xrange(self.result['maxRounds']):
			bla+=self.patternService.apply(self.result['champsValeurs'][i])

		return bla


class Service(object):
	def __init__(self,params):
		self.params	= params
		self.cleanName	= self.params['name'].replace(config.csvHeaderFs+config.csvHeaderDo,'')	# cleanName = name without ':do'


	def getName(self):
		return self.cleanName


	def DISABLED_loadServiceData(self):
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


	def DISABLED_buildArrayOfServices(self):
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
