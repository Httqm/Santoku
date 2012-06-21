#!/bin/bash

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


# TODO : add trap for CTRL-c

# config values for local host
localPathToFiles='./output'
logFile='./checkConf.log'

# config values for Shinken host
shinkenHost='192.168.1.101'
shinkenSshUser='root'
shinkenBaseFolder='/usr/local/shinken/'		# final '/' expected
shinkenEtcFolder=$shinkenBaseFolder'etc/'		# final '/' expected
backupSuffix='_PREVIOUS'

shinkenCheckBin=$shinkenBaseFolder'bin/shinken-arbiter'
shinkenRestartCmd='/etc/init.d/shinken restart'
shinkenConfigFile=$shinkenEtcFolder'nagios.cfg'

# misc
stringOk='[ OK ]'
stringKo='[ KO ]'


# Args :
# $1 : file to copy
# $2 : local folder on destination
function sshCopyToShinkenHost {
	backupFile $2$(basename $1)
#	echo -n "Copying $1 to $shinkenHost ........ "
	scp -q $1 $shinkenSshUser@$shinkenHost:$2 1>/dev/null 2>&1 || { echo "Can not copy $1 to $shinkenHost";exit 1; }
# TODO : improve error management
	}

# Args :
# $1 : absolute path to file to backup
function backupFile {
#	echo -n "Making a backup copy of $1 ........ "
#	ssh $shinkenSshUser@$shinkenHost "[ -f $1 ] && cp $1 $1$backupSuffix" && echo 'OK :-)' || 'KO :-('
	ssh $shinkenSshUser@$shinkenHost "[ -f $1 ] && cp $1 $1$backupSuffix"
	}

function checkShinkenConfig {
	ssh $shinkenSshUser@$shinkenHost "$shinkenCheckBin -v -c $shinkenConfigFile" 1>$logFile 2>&1
	}

function showCheckConfLog {
	echo $stringKo
	grep "Error:" $logFile
	echo
	echo "Read full details in $logFile"
	}

function restartShinken {
#	echo "RESTARTING SHINKEN ..."
	ssh $shinkenSshUser@$shinkenHost "$shinkenRestartCmd"
	}

# TODO : deploy either to an SSH host or to the local host
echo -n ' Copying files ............... '
sshCopyToShinkenHost $localPathToFiles/commands.cfg $shinkenEtcFolder
sshCopyToShinkenHost $localPathToFiles/hosts.cfg $shinkenEtcFolder'hosts/'
sshCopyToShinkenHost $localPathToFiles/services.cfg $shinkenEtcFolder'services/'
echo $stringOk

echo -n ' Checking configuration ...... '
#checkShinkenConfig && echo 'OK' || echo 'KO'
checkShinkenConfig && echo $stringOk || { showCheckConfLog;exit 1; }


echo -n ' Restarting Shinken .......... '
restartShinken && echo $stringOk || echo $stringKo



#r=$(checkShinkenConfig)
#checkShinkenConfig && echo 'OK' || echo 'KO'
#[ $(checkShinkenConfig) -eq 1 ] && restartShinken || showCheckConfLog

