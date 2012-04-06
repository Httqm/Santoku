#!/usr/bin/python

# source : http://stackoverflow.com/questions/3824455/python-constants
CONSTANT1 = "value1"
CONSTANT2 = "value2"


srcFileDir			= './config/'	# TODO : name files as path/to/file
srcFile				= 'file.csv'
srcFileFs			= ';'		# CSV field separator
srcFileParamFs			= '|'		# separator used when a CSV cell contains several values
hostFileIni			= 'host.ini'
hostGroupFileIni		= 'hostgroup.ini'
hostServiceDirectivesFileIni	= 'host_service_directives.ini'
#objHostGroupFileIni

outFileDir		= './output/'
outFileHosts		= 'hosts.cfg'
outFileServices		= 'services.cfg'
