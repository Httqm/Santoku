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

# Load data from 'host.ini'
objHostFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileHostIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHost	= objHostFileIni.getData()

# Load data from 'host_service_directives.ini'
objHostServiceDirectivesFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileDirectivesIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgHostDirectives		= objHostServiceDirectivesFileIni.getData()

# Load data from 'hostgroup.ini'
objHostGroupFileIni	= FileIni({
		'name'		: config.configFilesPath+config.fileHostgroupIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHostGroup	= objHostGroupFileIni.getData()


# Preparing for services. Detecting all '*:do' columns from the CSV
import re	# for RegExp
services=[]
for field in fileCsv.getHeader():
	match=re.search('.*:'+config.csvHeaderDo+'$', field)
	if(match):
		services.append(field)


########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
hostsOutput	= ''
hostGroups	= {}	# dict : hg name => hg members
servicesOutput	= ''


try:
	cfgDataHost[config.iniPatternString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniPatternString+'" not found in "'+objHostFileIni.name})

try:
	cfgDataHost[config.iniVarToTagString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+config.iniVarToTagString+'" not found in "'+objHostFileIni.name})


objPatternHost	= Pattern({
		'pattern' : cfgDataHost[config.iniPatternString],
		'variable2tag' : cfgDataHost[config.iniVarToTagString]
		})


objPatternDirectives	= Pattern({
		'pattern' : cfgHostDirectives[config.iniPatternString],
		'variable2tag' : cfgHostDirectives[config.iniVarToTagString]
		})


for host in csvData:	# 'host' is the key of the 'csvData' dict

	objHost		= Host(csvData[host])
	listHostGroups	= objHost.getHostGroups()

	# skip hosts marked as 'ignore_host'
	if(csvData[host]['ignore_host']=='1'):
		continue

	# load host directives for injection into csvData[host]
	try:
		csvData[host][config.csvHostDirectivesNames]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesNames+'" not found in "'+fileCsv.name+'"'})

	try:
		csvData[host][config.csvHostDirectivesValues]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+config.csvHostDirectivesValues+'" not found in "'+fileCsv.name+'"'})


	hostDirectives		= ''
	directivesNames		= csvData[host][config.csvHostDirectivesNames].split(config.csvMultiValuedCellFS)
	directivesValues	= csvData[host][config.csvHostDirectivesValues].split(config.csvMultiValuedCellFS)



	for index,value in enumerate(directivesNames):
		hostDirectives	+= objPatternDirectives.apply({	'directiveName' : directivesNames[index], 'directiveValue' : directivesValues[index]})

	# inject the host directives into the host data for use by the pattern
	csvData[host]['hostDirectives']	= hostDirectives	# <== HARDCODED field name. should avoid this!

	# 'normal' hosts data fields
	hostsOutput	+= objPatternHost.apply(csvData[host])

	# Store hosts into hostgroups
	for hg in listHostGroups:
		if not hg in hostGroups:	# if 'hostGroups[hg]' doesn't exist yet, create it.
			hostGroups[hg]=[]
		hostGroups[hg].append(host)	# then store 'host' in it !


	################################## ##########################################################
	# Looping on services
	################################## ##########################################################

	# detecting services to register
	# services is the list of all '*:do' CSV columns : ['check_filesystem:do', 'check_bidule:do']
	for service in services:

		# if 'do', load service stuff (pattern, csv2data, fields, values) and cook them together
		if(csvData[host][service]=='1'):

			serviceName=service.replace(':'+config.csvHeaderDo,'')
			################## ##########################################################
			# service directives
			################## ##########################################################
			# Making sure the current service has directives (names + values cells exist and are not empty)
			serviceDirectives	= ''
			hasDirectives		= 1

			for columnName in [serviceName+':'+config.csvServiceDirectivesNames, serviceName+':'+config.csvServiceDirectivesValues]:

				if(fileCsv.columnExists(columnName)):
					hasDirectives=hasDirectives and csvData[host][columnName]
				else:
					hasDirectives=0

			if(hasDirectives):
				# loading service directives from CSV data
				directivesNames		= csvData[host][serviceName+':'+config.csvServiceDirectivesNames].split(config.csvMultiValuedCellFS)
				directivesValues	= csvData[host][serviceName+':'+config.csvServiceDirectivesValues].split(config.csvMultiValuedCellFS)

				# applying the serviceDirectives pattern
				for name,value in enumerate(directivesNames):
					serviceDirectives+=objPatternDirectives.apply({
						'directiveName'		: directivesNames[name],
						'directiveValue'	: directivesValues[name]
						})

			################## ##########################################################
			# /service directives
			################## ##########################################################

			objService	= Service({
					'name'			: serviceName,
					'host'			: host,
					'csvHeader'		: fileCsv.getHeader(),
					'csvDataLine'		: csvData[host],
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

# Hosts
objFileOut	= FileOutput({ 'name' : config.outputPath+config.outputFileHosts })	# obj[ClassName] : name of instance
objFileOut.write(hostsOutput)

# Services
objFileOut	= FileOutput({ 'name' : config.outputPath+config.outputFileServices })	# obj[ClassName] : name of instance
objFileOut.write(servicesOutput)


########################################## ##########################################################
# the end!
########################################## ##########################################################
