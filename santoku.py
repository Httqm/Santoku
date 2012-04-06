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


# making local names for imported classes
FileInCsv	= fichier.FileInCsv
FileInIni	= fichier.FileInIni
FileOut		= fichier.FileOut
Pattern		= pattern.Pattern

Host		= hosts.Host
Service		= services.Service


########################################## ##########################################################
# main()
########################################## ##########################################################

# Load host data from CSV
objFileInCsv	= FileInCsv({ 'name' : c.srcFile, 'fs' : c.srcFileFs })	# obj[ClassName] : name of instance
csvData		= objFileInCsv.getData()


# Load data from 'host.ini'
objHostFileIni	= FileInIni({ 'name' : c.srcFileDir+c.hostFileIni })
cfgDataHost	= objHostFileIni.getData()


# Load data from 'host_service_directives.ini'
objHostServiceDirectivesFileIni	= FileInIni({ 'name' : c.srcFileDir+c.hostServiceDirectivesFileIni })
cfgHostDirectives		= objHostServiceDirectivesFileIni.getData()



# Load data from 'hostgroup.ini'
objHostGroupFileIni	= FileInIni({ 'name' : c.srcFileDir+c.hostGroupFileIni })
cfgDataHostGroup	= objHostGroupFileIni.getData()


# Preparing for services. Detecting all '*:do' columns from the CSV
import re	# for RegExp
services=[]
for field in objFileInCsv.getHeader():
#	print field
	match=re.search('.*:do$', field)
	if(match):
#		print field+' MATCHES ---------------------------------'
		services.append(field)


########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
hostsOutput	= ''
hostGroups	= {}	# dict : hg name => hg members
servicesOutput	= ''


objPatternHost		= Pattern({ 'pattern' : cfgDataHost['pattern'], 'variable2tag' : cfgDataHost['VARIABLE2TAG'] })
objPatternDirectives	= Pattern({ 'pattern' : cfgHostDirectives['pattern'], 'variable2tag' : cfgHostDirectives['VARIABLE2TAG'] })

for host in csvData:	# 'host' is a line of the CSV data

	objHost		= Host(csvData[host])
	listHostGroups	= objHost.getHostGroups()

	# skip hosts marked as 'ignore_host'
	if(csvData[host]['ignore_host']=='1'):
		continue

	# load host directives for injection into csvData[host]
	hostDirectives		= ''
	directivesNames		= csvData[host]['hostDirective_name'].split('|')
	directivesValues	= csvData[host]['hostDirective_value'].split('|')

	for index,value in enumerate(directivesNames):
		hostDirectives+=objPatternDirectives.apply({ 'directiveName' : directivesNames[index], 'directiveValue' : directivesValues[index]})

	# inject the host directives into the host data for use by the pattern
	csvData[host]['hostDirectives']=hostDirectives	# <== HARDCODED field name. should avoid this!

	# 'normal' hosts data fields
	hostsOutput+=objPatternHost.apply(csvData[host])

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
#			serviceName	= service.replace(':do','')	# <== HARDCODED. bad!

			objService	= Service({
					'name'			: service.replace(':do',''),
					'host'			: host,
					'csvHeader'		: objFileInCsv.getHeader(),
					'csvDataLine'		: csvData[host],
					'fieldSeparator'	: c.srcFileParamFs
					})

			result	= objService.buildArrayOfServices()


			"""
#			print '+++++++Loading '+serviceName

			# retrieving service fields and values for this host from CSV
			champsValeurs	= {}
			serviceCsvData={} # temporary dict

			# storing CSV data in a dict to play with it later
			for field in objFileInCsv.getHeader():
				match=re.search(serviceName+':.*', field)
				if(match):
					# parsing all CSV columns related to this service
					serviceCsvData[field.replace(serviceName+':','')]=csvData[host][field]

#			print serviceCsvData

			# Parsing data stored in dict to register as many services as the number of values in mutli-valued cells
			maxRounds	= 1
			currentRound	= 0

			while currentRound < maxRounds:
				champsValeurs[currentRound]	= {
					'host_name'	: csvData[host]['host_name'],
					'use'		: 'generic_service'
					}
				for serviceField in serviceCsvData:
#					print 'FIELD : DATA         '+serviceField+' '+serviceCsvData[serviceField]
					valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(c.srcFileParamFs)
					maxRounds		= len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds
					try:
						tmpValue	= valuesOfMultiValuedCell[currentRound]
					except IndexError:
						tmpValue	= valuesOfMultiValuedCell[0]
#					print 'valuesOfMultiValuedCell['+str(currentRound)+'] = '+tmpValue+', '+str(len(valuesOfMultiValuedCell))
					print serviceField+' : '+tmpValue

					champsValeurs[currentRound][serviceField]=tmpValue

				currentRound+=1
			print champsValeurs
			"""



			# Load service data from './config/"serviceName".ini'
			objServiceFileIni	= FileInIni({ 'name' : c.srcFileDir+objService.getName()+'.ini' })

			cfgDataService		= objServiceFileIni.getData()

			objPatternService	= Pattern({ 'pattern' : cfgDataService['pattern'], 'variable2tag' : cfgDataService['VARIABLE2TAG'] })

			# finally apply service pattern as many time as the maximum number of values in multi-valued CSV cells
			for i in xrange(result['maxRounds']):
				servicesOutput+=objPatternService.apply(result['champsValeurs'][i])

"""
print '++++++++++++++++++++'
print servicesOutput
print '++++++++++++++++++++'
"""

#print 'HOSTGROUPS'
#print hostGroups

# host loop done : we've seen all hosts. Let's build hostgroups
objPatternHost=Pattern({ 'pattern' : cfgDataHostGroup['pattern'], 'variable2tag' : cfgDataHostGroup['VARIABLE2TAG'] })


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

"""

# for services
paramsOutServices={
	'name'	: c.outFileDir+outFileServices,
	}
"""

########################################## ##########################################################
# the end!
########################################## ##########################################################
