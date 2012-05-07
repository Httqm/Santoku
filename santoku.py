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


# Python basics : http://www.astro.ufl.edu/~warner/prog/python.html

########################################## ##########################################################
# IMPORTS
########################################## ##########################################################
# http://www.sthurlow.com/python/lesson09/
# source : http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder

from modules import config
from modules import pattern	# imported from ./modules/pattern.py
from modules import fichier
from modules import hosts
from modules import services
from modules import controller

# For code readabiliy, making local names for imported classes
FileCsv		= fichier.FileCsv
FileIni		= fichier.FileIni
FileOutput	= fichier.FileOutput
Pattern		= pattern.Pattern
Controller	= controller.Controller

AllHosts	= hosts.AllHosts
Host		= hosts.Host
Service		= services.Service


########################################## ##########################################################
# main()
########################################## ##########################################################

controller	= Controller()


# Load host data from CSV
fileCsv	= FileCsv({
		'name'		: config.csvFileName,
		'fs'		: config.csvFileFs,
		'controller'	: controller
		})
csvData		= fileCsv.getData()


"""
#START
# Load data from 'host.ini'
fileIniHost	= FileIni({
		'name'		: config.configFilesPath+config.fileHostIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHost	= fileIniHost.getData()
#STOP
"""

"""
# Load data from 'host_service_directives.ini'
objHostServiceDirectivesFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileDirectivesIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgHostDirectives		= objHostServiceDirectivesFileIni.getData()
"""

# Load data from 'hostgroup.ini'
objHostGroupFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileHostgroupIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHostGroup	= objHostGroupFileIni.getData()


# Preparing for services. Detecting all '*:do' columns from the CSV
import re	# for RegExp
serviceList=[]
for field in fileCsv.getHeader():
	match=re.search('.*:'+config.csvHeaderDo+'$', field)
	if(match):
		serviceList.append(field)


########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
hostsOutput	= ''
hostGroups	= {}	# dict : hg name => hg members
servicesOutput	= ''


"""
#START
try:
	cfgDataHost[config.iniPatternString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+fileIniHost.name})
try:
	cfgDataHost[config.iniVarToTagString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+fileIniHost.name})
#STOP
"""


"""
#START
objPatternHost	= Pattern({
		'pattern'	: cfgDataHost[config.iniPatternString],
		'variable2tag'	: cfgDataHost[config.iniVarToTagString]
		})

objPatternDirectives	= Pattern({
		'pattern'	: cfgHostDirectives[config.iniPatternString],
		'variable2tag'	: cfgHostDirectives[config.iniVarToTagString]
		})
#STOP
"""
allHosts=AllHosts()
allHosts.loadIniFiles()
allHosts.loadPatterns()


for hostName in csvData:	# 'hostName' is the key of the 'csvData' dict

	host		= Host({
			'data'		: csvData[hostName],
			'csvFileName'	: fileCsv.name,
			'controller'	: controller,
#			'pattern'	: objPatternDirectives,
			'allHosts'	: allHosts
			})

	listHostGroups	= host.getHostGroups()

	if(host.isMarkedToBeIgnored()):
		continue

	# load host directives for injection into csvData[hostName]
	"""
	#START
	try:
		csvData[hostName][config.csvHostDirectivesNames]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesNames+'" not found in "'+fileCsv.name+'"'})

	try:
		csvData[hostName][config.csvHostDirectivesValues]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesValues+'" not found in "'+fileCsv.name+'"'})


	hostDirectives		= ''
	directivesNames		= csvData[hostName][config.csvHostDirectivesNames].split(config.csvMultiValuedCellFS)
	directivesValues	= csvData[hostName][config.csvHostDirectivesValues].split(config.csvMultiValuedCellFS)



	for index,value in enumerate(directivesNames):
		hostDirectives	+= objPatternDirectives.apply({	'directiveName' : directivesNames[index], 'directiveValue' : directivesValues[index]})
	print '============'
	print hostDirectives

	# inject the host directives into the host data for use by the pattern
	csvData[hostName]['hostDirectives']	= hostDirectives	# <== HARDCODED field name. should avoid this!
	#STOP
	"""
	csvData[hostName]['hostDirectives']	= host.loadDirectives()


	# 'normal' hosts data fields
#	hostsOutput	+= objPatternHost.apply(csvData[hostName])
	hostsOutput	+= host.applyHostPattern(csvData[hostName])

	# Store hosts into hostgroups
	for hg in listHostGroups:
		if not hg in hostGroups:	# if 'hostGroups[hg]' doesn't exist yet, create it.
			hostGroups[hg]=[]
		hostGroups[hg].append(hostName)	# then store 'host' in it !


	################################## ##########################################################
	# Looping on services
	################################## ##########################################################

	# detecting services to register
	# serviceList is the list of all '*:do' CSV columns : ['check_filesystem:do', 'check_bidule:do']
	for singleServiceCsvName in serviceList:

		service=services.Service2({
				'currentCsvLine'	: csvData[hostName],
				'serviceCsvName'	: singleServiceCsvName
				})

		# if 'do', load service stuff (pattern, csv2data, fields, values) and cook them together
		#if(csvData[hostName][singleServiceCsvName]=='1'):
		if service.isEnabled():

			#serviceName=singleServiceCsvName.replace(config.csvHeaderFs+config.csvHeaderDo,'')
			serviceName=service.getName()
			################## ##########################################################
			# service directives
			################## ##########################################################
			# Making sure the current service has directives (names + values cells exist and are not empty)

			if service.hasDirectives(fileCsv):
#				print 'HAS DIRECTIVES'

				"""
				#START
				hasDirectives		= 1

				for columnName in [serviceName+config.csvHeaderFs+config.csvServiceDirectivesNames, serviceName+config.csvHeaderFs+config.csvServiceDirectivesValues]:

					if(fileCsv.columnExists(columnName)):
						hasDirectives=hasDirectives and csvData[hostName][columnName]
					else:
						hasDirectives=0

				if(hasDirectives):
				#END
				"""

				"""
				#START
				# loading service directives from CSV data
				directivesNames	= csvData[hostName][serviceName+config.csvHeaderFs+config.csvServiceDirectivesNames].split(config.csvMultiValuedCellFS)
				directivesValues= csvData[hostName][serviceName+config.csvHeaderFs+config.csvServiceDirectivesValues].split(config.csvMultiValuedCellFS)

				#END
				"""

				service.loadDirectivesFromCsvData()

				serviceDirectives=service.applyServiceDirectivesPattern()

				"""
				#START
				# applying the serviceDirectives pattern
				serviceDirectives	= ''

				for name,value in enumerate(directivesNames):
					serviceDirectives+=objPatternDirectives.apply({
						'directiveName'		: directivesNames[name],
						'directiveValue'	: directivesValues[name]
						})
				#END
				"""

			################## ##########################################################
			# /service directives
			################## ##########################################################

			objService	= Service({
					'name'			: serviceName,
					'hostName'		: hostName,
					'csvHeader'		: fileCsv.getHeader(),
					'csvDataLine'		: csvData[hostName],
					'fieldSeparator'	: config.csvFileParamFs,
					'serviceDirectives'	: serviceDirectives
					})

			result	= objService.buildArrayOfServices()

			# Load service data from './config/"serviceName".ini'
			objServiceFileIni	= FileIni({
					'name'		: config.configFilesPath+objService.getName()+'.ini',
					'fs'		: '',
					'controller'	: controller
					})

			# Load INI file data
			cfgDataService		= objServiceFileIni.getData()



			try:
				cfgDataService[config.iniPatternString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+objServiceFileIni.name})

			try:
				cfgDataService[config.iniVarToTagString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+objServiceFileIni.name})


			objPatternService	= Pattern({
					'pattern' : cfgDataService[config.iniPatternString],
					'variable2tag' : cfgDataService[config.iniVarToTagString]
					})

			# finally apply service pattern as many time as the maximum number of values in multi-valued CSV cells
			for i in xrange(result['maxRounds']):
				servicesOutput+=objPatternService.apply(result['champsValeurs'][i])


# host loop done : we've seen all hosts. Let's build hostgroups
try:
	objPatternHost=Pattern({
			'pattern'	: cfgDataHostGroup[config.iniPatternString],
			'variable2tag'	: cfgDataHostGroup[config.iniVarToTagString]
			})
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" doesn\'t exist in "'+objHostGroupFileIni.name+'"' })



for hostgroup_name in hostGroups:
	HG			= {}
	members			= ', '.join(hostGroups[hostgroup_name])	# hosts of the hostgroup_name, as a string
	HG['hostgroup_name']	= hostgroup_name
	HG['alias']		= hostgroup_name
	HG['members']		= members

	hostsOutput+=objPatternHost.apply(HG)
	

########################################## ##########################################################
# Write results to files
########################################## ##########################################################

outputFileHosts		= FileOutput({ 'name' : config.outputPath+config.outputFileHosts })
outputFileHosts.write(hostsOutput)

outputFileServices	= FileOutput({ 'name' : config.outputPath+config.outputFileServices })
outputFileServices.write(servicesOutput)


########################################## ##########################################################
# the end!
########################################## ##########################################################
