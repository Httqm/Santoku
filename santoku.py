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
from modules import controller
from modules import fichier
from modules import hosts
from modules import hostgroups
from modules import pattern
from modules import services

# local names for imported classes
AllHosts	= hosts.AllHosts
Controller	= controller.Controller
FileCsv		= fichier.FileCsv
FileIni		= fichier.FileIni
FileOutput	= fichier.FileOutput
Hostgroups	= hostgroups.Hostgroups
Pattern		= pattern.Pattern
Host		= hosts.Host
Service		= services.Service
AllServices	= services.AllServices

########################################## ##########################################################
# main()
########################################## ##########################################################

controller	= Controller()

# Load host data from CSV
fileCsv	= FileCsv({
		'name'	: config.csvFileName,
		'fs'	: config.csvFileFs
		})
csvData		= fileCsv.getData()


allHosts	= AllHosts()
hostgroups	= Hostgroups()
allServices	= AllServices()
serviceList	= allServices.getList(fileCsv.getHeader())


########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
for hostName in csvData:	# 'hostName' is the key of the 'csvData' dict

	host	= Host({
		'data'		: csvData[hostName],
		'csvFileName'	: fileCsv.name,
		'controller'	: controller,
		'allHosts'	: allHosts
		})

	groupsHostBelongsTo	= host.loadHostGroupsFromCsv()

	if host.isMarkedToBeIgnored() :
		continue

	csvData[hostName]['hostDirectives']	= host.loadDirectives()

	# 'normal' hosts data fields
	allHosts.output	+= host.applyHostPattern(csvData[hostName])

	hostgroups.addHostToGroups({
		'host'		: hostName,
		'groups'	: groupsHostBelongsTo
		})

	################################## ##########################################################
	# Looping on services
	################################## ##########################################################

	# detecting services to register
	# serviceList is the list of all '*:do' CSV columns : ['check_filesystem:do', 'check_bidule:do']
	for singleServiceCsvName in serviceList:

		service=Service({
				'currentCsvLine'	: csvData[hostName],
				'serviceCsvName'	: singleServiceCsvName
				})

		if service.isEnabled():

			serviceName	= service.getName()

			# service directives
			if service.hasDirectives(fileCsv):
				service.loadDirectivesFromCsvData()
				serviceDirectives	= service.applyServiceDirectivesPattern()
			# /service directives

			result	= service.buildArrayOfServices({
					'name'			: serviceName,
					'hostName'		: hostName,
					'csvHeader'		: fileCsv.getHeader(),
					'csvDataLine'		: csvData[hostName],
					'serviceDirectives'	: serviceDirectives
					})


			allServices.output+=service.make()


# host loop done : we've seen all hosts. Let's build hostgroups
allHosts.output+=hostgroups.make()
	

########################################## ##########################################################
# Write results to files
########################################## ##########################################################

outputFileHosts		= FileOutput({ 'name' : config.outputPath+config.outputFileHosts })
outputFileHosts.write(allHosts.output)

outputFileServices	= FileOutput({ 'name' : config.outputPath+config.outputFileServices })
outputFileServices.write(allServices.output)


########################################## ##########################################################
# the end!
########################################## ##########################################################
