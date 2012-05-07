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
from modules import pattern
from modules import fichier
from modules import hosts
from modules import services
from modules import controller
from modules import hostgroups

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
# Load data from 'hostgroup.ini'
objHostGroupFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileHostgroupIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHostGroup	= objHostGroupFileIni.getData()
"""


allServices	= services.AllServices()
serviceList	= allServices.getList(fileCsv.getHeader())

########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
hostsOutput	= ''
servicesOutput	= ''

hostgroups=hostgroups.Hostgroups()
#hostGroups	= {}	# dict : hg name => hg members


allHosts=AllHosts()
allHosts.loadIniFiles()
allHosts.loadPatterns()


for hostName in csvData:	# 'hostName' is the key of the 'csvData' dict

	host	= Host({
		'data'		: csvData[hostName],
		'csvFileName'	: fileCsv.name,
		'controller'	: controller,
		'allHosts'	: allHosts
		})

	listHostGroups	= host.loadHostGroupsFromCsv()

	if(host.isMarkedToBeIgnored()):
		continue

	csvData[hostName]['hostDirectives']	= host.loadDirectives()

	# 'normal' hosts data fields
	hostsOutput	+= host.applyHostPattern(csvData[hostName])


	# Store hosts into hostgroups
	hostgroups.addHostToGroups({
		'host'		: hostName,
		'groups'	: listHostGroups
		})
	"""
	for hg in listHostGroups:
		if not hg in hostGroups:	# if 'hostGroups[hg]' doesn't exist yet, create it.
			hostGroups[hg]=[]
		hostGroups[hg].append(hostName)	# then store 'host' in it !
	"""

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
			if service.hasDirectives(fileCsv):

				service.loadDirectivesFromCsvData()

				serviceDirectives=service.applyServiceDirectivesPattern()


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
hostsOutput+=hostgroups.make()
	

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
