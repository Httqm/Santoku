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


########################################## ##########################################################
# FILES AND FOLDERS
########################################## ##########################################################
# common
##configFile          = __file__  # This is used to point to THIS file in error messages. DON'T CHANGE THIS !
configFilesPath     = './config/'

# CSV file
csvFileName     = 'home.csv'
###csvFileName    = 'file.csv'
###csvFileName    = 'hostsOBS.csv'
###csvFileName    = 'hostsOBS_light.csv'
csvFileFs       = ';'   # CSV field separator. Must be different from the CSV list separator below.
##csvFileParamFs  = '|'   # CSV list separator. This is used when a CSV cell contains several values

# INI files
fileHostIni         = 'host.ini'
fileHostgroupIni    = 'hostgroup.ini'
fileDirectivesIni   = 'directives.ini'
fileSummaryIni      = 'summary.ini'

# OUTPUT files
outputPath          = './output/'
outputFileHosts     = 'hosts.cfg'
outputFileServices  = 'services.cfg'
outputFileCommands  = 'commands.cfg'


########################################## ##########################################################
# OUTPUT MESSAGES & DEBUG
########################################## ##########################################################
messageDie  = 'Tenno Heika Banzai !!! (seppuku...)'
debug       = 1 # 0|1, enable output of controller.showDebug messages

########################################## ##########################################################
# CSV COSMETICS
# You needn't change these values : Santoku works fine as is.
# Values are defined here to avoid hardcoded strings.
# But just in case you don't like the way they are (cosmetics) or need a workaround for any reason :
# HAVE FUN !
########################################## ##########################################################
csvMultiValuedCellFS        = '|'
csvHeaderDo                 = 'do'
csvHeaderFs                 = ':'
csvHeaderHostName           = 'host_name'
csvHeaderIgnoreHost         = 'ignore_host'
csvHeaderCheckCommand       = 'check_command'
csvHeaderUse                = 'use'
csvHeaderHostgroups         = 'hostgroups'
csvGenericService           = 'generic_service'
csvHostDirectivesNames      = 'hostDirectivesNames'
csvHostDirectivesValues     = 'hostDirectivesValues'
csvServiceDirectivesNames   = 'serviceDirectivesNames'
csvServiceDirectivesValues  = 'serviceDirectivesValues'


########################################## ##########################################################
# INI COSMETICS
# You needn't change these values : Santoku works fine as is.
# Values are defined here to avoid hardcoded strings.
# But just in case you don't like the way they are (cosmetics) or need a workaround for any reason :
# HAVE FUN !
########################################## ##########################################################
iniPatternString    = 'PATTERN'
##iniVarToTagString   = 'VARIABLE2TAG'
##iniVarToTagStanzaFs = '='
iniCommandString    = 'COMMAND'
iniTagChar          = '$'

############################################ ##########################################################
### NAGIOS / SHINKEN .cfg DIRECTIVES
### Values below are there just to avoid hardcoding.
###
### DON'T CHANGE THIS !
############################################ ##########################################################
##commandDirectiveInServiceDefinition	= 'check_command'
##commandDirectiveInCommandDefinition	= 'command_name'
##defaultCommands="""
##define command {
##	command_name	notify-host-by-email
##	command_line	/usr/bin/printf "%b" "Shinken Notification\n\nType:$NOTIFICATIONTYPE$\nHost: $HOSTNAME$\nState: $HOSTSTATE$\nAddress: $HOSTADDRESS$\nInfo: $HOSTOUTPUT$\nDate/Time: $SHORTDATETIME$" | /usr/bin/mail -s "Host $HOSTNAME$	is	$HOSTSTATE$" $CONTACTEMAIL$
##	}
##
##define command {
##	command_name	notify-service-by-email
##	command_line	/usr/bin/printf "%b" "Shinken Notification\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $SHORTDATETIME$ Additional Info : $SERVICEOUTPUT$" | /usr/bin/mail -s "$NOTIFICATIONTYPE$	$HOSTALIAS$ / $SERVICEDESC$	$SERVICESTATE$" $CONTACTEMAIL$
##	}
##"""
