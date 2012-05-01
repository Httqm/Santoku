#!/usr/bin/python

# source : http://stackoverflow.com/questions/3824455/python-constants

########################################## ##########################################################
# FILES AND FOLDERS
########################################## ##########################################################
srcFileDir			= './config/'	# TODO : name files as path/to/file
#srcFile				= 'hosts.csv'
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

configFile		= __file__	# This is use to point to this file in error messages, don't change it !

########################################## ##########################################################
# FILES AND FOLDERS
########################################## ##########################################################
messageDie		= 'Tennoheika, banzai !!! (seppuku...)'
# https://en.wikipedia.org/wiki/Seppuku
# http://www.squidoo.com/seppuku

########################################## ##########################################################
# CSV COSMETICS
# You needn't change these values : Santoku works fine as is.
# Values are defined here to avoid hardcoded string in the code.
# But just in case you don't like the way they are (cosmetics) or need a workaround for any reason :
# HAVE FUN !
########################################## ##########################################################
csvMultiValuedCellFS		= '|'
csvHeaderDo			= 'do'
csvHeaderHostName		= 'host_name'
csvHeaderUse			= 'use'
csvGenericService		= 'generic_service'
csvHostDirectivesNames		= 'hostDirectivesNames'
csvHostDirectivesValues		= 'hostDirectivesValues'
csvServiceDirectivesNames	= 'serviceDirectivesNames'
csvServiceDirectivesValues	= 'serviceDirectivesValues'



########################################## ##########################################################
# INI COSMETICS
# You needn't change these values : Santoku works fine as is.
# Values are defined here to avoid hardcoded string in the code.
# But just in case you don't like the way they are (cosmetics) or need a workaround for any reason :
# HAVE FUN !
########################################## ##########################################################
iniPatternString	= 'pattern'
iniVarToTagString	= 'VARIABLE2TAG'
