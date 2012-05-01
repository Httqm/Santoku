#!/usr/bin/python

# Python basics : http://www.astro.ufl.edu/~warner/prog/python.html

########################################## ##########################################################
# IMPORTS
########################################## ##########################################################
# http://www.sthurlow.com/python/lesson09/
# source : http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder

from modules import config as c

from modules import pattern	# imported from ./modules/pattern.py
from modules import fichier
from modules import hosts
from modules import services
from modules import controller

# making local names for imported classes
FileInCsv	= fichier.FileInCsv
FileInIni	= fichier.FileInIni
FileOut		= fichier.FileOut
Pattern		= pattern.Pattern
Controller	= controller.Controller

Host		= hosts.Host
Service		= services.Service


########################################## ##########################################################
# main()
########################################## ##########################################################

controller	= Controller()


# Load host data from CSV
objFileInCsv	= FileInCsv({
		'name'		: c.srcFile,
		'fs'		: c.srcFileFs,
		'controller'	: controller
		})
csvData		= objFileInCsv.getData()

# Load data from 'host.ini'
objHostFileIni	= FileInIni({
		'name'		: c.srcFileDir+c.hostFileIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHost	= objHostFileIni.getData()

# Load data from 'host_service_directives.ini'
objHostServiceDirectivesFileIni	= FileInIni({
		'name'		: c.srcFileDir+c.hostServiceDirectivesFileIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgHostDirectives		= objHostServiceDirectivesFileIni.getData()

# Load data from 'hostgroup.ini'
objHostGroupFileIni	= FileInIni({
		'name'		: c.srcFileDir+c.hostGroupFileIni,
		'fs'		: '',
		'controller'	: controller
		})
cfgDataHostGroup	= objHostGroupFileIni.getData()


# Preparing for services. Detecting all '*:do' columns from the CSV
import re	# for RegExp
services=[]
for field in objFileInCsv.getHeader():
	match=re.search('.*:'+c.csvHeaderDo+'$', field)
	if(match):
		services.append(field)


########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
hostsOutput	= ''
hostGroups	= {}	# dict : hg name => hg members
servicesOutput	= ''


try:
	cfgDataHost[c.iniPatternString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+c.iniPatternString+'" not found in "'+objHostFileIni.name})

try:
	cfgDataHost[c.iniVarToTagString]
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+c.iniVarToTagString+'" not found in "'+objHostFileIni.name})


objPatternHost	= Pattern({
		'pattern' : cfgDataHost[c.iniPatternString],
		'variable2tag' : cfgDataHost[c.iniVarToTagString]
		})


objPatternDirectives	= Pattern({
		'pattern' : cfgHostDirectives[c.iniPatternString],
		'variable2tag' : cfgHostDirectives[c.iniVarToTagString]
		})


for host in csvData:	# 'host' is the key of the 'csvData' dict

	objHost		= Host(csvData[host])
	listHostGroups	= objHost.getHostGroups()

	# skip hosts marked as 'ignore_host'
	if(csvData[host]['ignore_host']=='1'):
		continue

	# load host directives for injection into csvData[host]
	try:
		csvData[host][c.csvHostDirectivesNames]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+c.csvHostDirectivesNames+'" not found in "'+objFileInCsv.name+'"'})

	try:
		csvData[host][c.csvHostDirectivesValues]
	except KeyError:
		controller.die({ 'exitMessage' : 'Key error : key "'+c.csvHostDirectivesValues+'" not found in "'+objFileInCsv.name+'"'})


	hostDirectives		= ''
	directivesNames		= csvData[host][c.csvHostDirectivesNames].split(c.csvMultiValuedCellFS)
	directivesValues	= csvData[host][c.csvHostDirectivesValues].split(c.csvMultiValuedCellFS)



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

			serviceName=service.replace(':'+c.csvHeaderDo,'')
			################## ##########################################################
			# service directives
			################## ##########################################################
			# Making sure the current service has directives (names + values cells exist and are not empty)
			serviceDirectives	= ''
			hasDirectives		= 1

			for columnName in [serviceName+':'+c.csvServiceDirectivesNames, serviceName+':'+c.csvServiceDirectivesValues]:

				if(objFileInCsv.columnExists(columnName)):
					hasDirectives=hasDirectives and csvData[host][columnName]
				else:
					hasDirectives=0

			if(hasDirectives):
				# loading service directives from CSV data
				directivesNames		= csvData[host][serviceName+':'+c.csvServiceDirectivesNames].split(c.csvMultiValuedCellFS)
				directivesValues	= csvData[host][serviceName+':'+c.csvServiceDirectivesValues].split(c.csvMultiValuedCellFS)

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
					'csvHeader'		: objFileInCsv.getHeader(),
					'csvDataLine'		: csvData[host],
					'fieldSeparator'	: c.srcFileParamFs,
					'serviceDirectives'	: serviceDirectives
					})

			result	= objService.buildArrayOfServices()

			# Load service data from './config/"serviceName".ini'
			objServiceFileIni	= FileInIni({
					'name'		: c.srcFileDir+objService.getName()+'.ini',
					'fs'		: '',
					'controller'	: controller
					})

			# Load INI file data
			cfgDataService		= objServiceFileIni.getData()



			try:
				cfgDataService[c.iniPatternString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+c.iniPatternString+'" not found in "'+objServiceFileIni.name})

			try:
				cfgDataService[c.iniVarToTagString]
			except KeyError:
				controller.die({ 'exitMessage' : 'Key error  : key "'+c.iniVarToTagString+'" not found in "'+objServiceFileIni.name})


			objPatternService	= Pattern({
					'pattern' : cfgDataService[c.iniPatternString],
					'variable2tag' : cfgDataService[c.iniVarToTagString]
					})





			# finally apply service pattern as many time as the maximum number of values in multi-valued CSV cells
			for i in xrange(result['maxRounds']):
				servicesOutput+=objPatternService.apply(result['champsValeurs'][i])


# host loop done : we've seen all hosts. Let's build hostgroups
try:
	objPatternHost=Pattern({
			'pattern'	: cfgDataHostGroup[c.iniPatternString],
			'variable2tag'	: cfgDataHostGroup[c.iniVarToTagString]
			})
except KeyError:
	controller.die({ 'exitMessage' : 'Key error  : key "'+c.iniPatternString+'" doesn\'t exist in "'+objHostGroupFileIni.name+'"' })



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
objFileOut	= FileOut({ 'name' : c.outFileDir+c.outFileHosts })	# obj[ClassName] : name of instance
objFileOut.write(hostsOutput)

# Services
objFileOut	= FileOut({ 'name' : c.outFileDir+c.outFileServices })	# obj[ClassName] : name of instance
objFileOut.write(servicesOutput)


########################################## ##########################################################
# the end!
########################################## ##########################################################
