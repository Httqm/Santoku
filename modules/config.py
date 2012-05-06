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


# source : http://stackoverflow.com/questions/3824455/python-constants

########################################## ##########################################################
# FILES AND FOLDERS
########################################## ##########################################################

configFilesPath		= './config/'	# TODO : name files as path/to/file

# CSV file
csvFileName		= 'file.csv'
csvFileFs		= ';'		# CSV field separator
csvFileParamFs		= '|'		# separator used when a CSV cell contains several values

# INI files
fileHostIni		= 'host.ini'
fileHostgroupIni	= 'hostgroup.ini'
fileDirectivesIni	= 'directives.ini'

# OUTPUT files
outputPath		= './output/'
outputFileHosts		= 'hosts.cfg'
outputFileServices	= 'services.cfg'

configFile		= __file__	# This is used to point to THIS file in error messages, don't change it !

########################################## ##########################################################
# OUTPUT MESSAGES
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
iniVarToTagStanzaFs	= '='
