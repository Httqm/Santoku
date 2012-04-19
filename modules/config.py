#!/usr/bin/python

# source : http://stackoverflow.com/questions/3824455/python-constants

########################################## ##########################################################
# FILES AND FOLDERS
########################################## ##########################################################
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

########################################## ##########################################################
# CSV COSMETICS
# You needn't change these values : Santoku works fine as is. But just in case you don't like
# the way they are (cosmetics) or need a workaround for any reason : have fun !
########################################## ##########################################################
# do : 
csvMultiValuedCellFS	= '|'
csvHeaderDo		= 'do'
