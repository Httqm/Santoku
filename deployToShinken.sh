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


trap "echo;echo 'Interrupted by CTRL-c.';exit 1;" INT


########################################## ##########################################################
# CONFIG
########################################## ##########################################################
useSsh=1		# If 1, deliver files through SSH. Otherwise simply 'cp' them.

# config values for local host
sourceFolder='./output/'											# final '/' expected
logFile='./checkConf.log'

# config values for Shinken host
shinkenHost='192.168.1.101'										# unused if Shinken host == localhost
shinkenSshUser='root'												# unused if Shinken host == localhost

shinkenBaseFolder='/usr/local/shinken/'						# final '/' expected
shinkenEtcFolder=$shinkenBaseFolder'etc/'						# final '/' expected
shinkenEtcHostsFolder=$shinkenEtcFolder'hosts/'				# final '/' expected
shinkenEtcServicesFolder=$shinkenEtcFolder'services/'		# final '/' expected

backupSuffix='_PREVIOUS_VERSION'


shinkenCheckBin=$shinkenBaseFolder'bin/shinken-arbiter'
shinkenRestartCmd='/etc/init.d/shinken restart'
shinkenConfigFile=$shinkenEtcFolder'nagios.cfg'

# misc
stringOk='[ OK ]'
stringKo='[ KO ]'


########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################

# Args :
# $1 : file or folder to check
function checkFileOrFolderExists {
	if [ $useSsh -eq 1 ]; then
		ssh $shinkenSshUser@$shinkenHost "[ -e \"$1\" ]" && : || { echo " $stringKo : the remote file or folder \"$1\" doesn't exist.";exit 1; }
	else
		[ -e "$1" ] && : || { echo " $stringKo : the local file or folder \"$1\" doesn't exist.";exit 1; }
	fi
	}


# Args :
# $1 : file to copy
# $2 : destination folder (either on localhost or on Shinken host)
function copyFileToShinkenFileTree {
	backupFile $2$(basename $1)

	if [ $useSsh -eq 1 ]; then
		scp -q "$1" $shinkenSshUser@$shinkenHost:"$2" 1>/dev/null 2>&1 || { echo "Can not copy \"$1\" to $shinkenHost";exit 1; }
	else
		cp $1 $2
	fi
	}


# Args :
# $1 : absolute path to file to backup
function backupFile {
	command="[ -f \"$1\" ] && cp \"$1\" \"$1$backupSuffix\""
	if [ $useSsh -eq 1 ]; then
		ssh $shinkenSshUser@$shinkenHost "$command"
	else
		$(command)
	fi
	}


function checkShinkenConfig {
	command="$shinkenCheckBin -v -c $shinkenConfigFile 1>$logFile 2>&1"
	if [ $useSsh -eq 1 ]; then
		ssh $shinkenSshUser@$shinkenHost "$command"
	else
		 echo $command
		$(command)
	fi
	}


function restartShinken {
	if [ $useSsh -eq 1 ]; then
		ssh $shinkenSshUser@$shinkenHost "$shinkenRestartCmd"
	else
		$shinkenRestartCmd
	fi
	}


function showCheckConfLog {
	echo $stringKo
	grep "Error:" $logFile
	echo
	echo "Read full details in $logFile"
	}


########################################## ##########################################################
# main()
########################################## ##########################################################

for fileOrFolder in "$shinkenEtcFolder" "$shinkenEtcHostsFolder" "$shinkenEtcServicesFolder" "$shinkenCheckBin" "$shinkenConfigFile";do
	checkFileOrFolderExists "$fileOrFolder"
done


echo -n ' Copying files ............... '
copyFileToShinkenFileTree ${sourceFolder}commands.cfg $shinkenEtcFolder
copyFileToShinkenFileTree ${sourceFolder}hosts.cfg $shinkenEtcHostsFolder
copyFileToShinkenFileTree ${sourceFolder}services.cfg $shinkenEtcServicesFolder
echo $stringOk


echo -n ' Checking configuration ...... '
checkShinkenConfig && echo $stringOk || { showCheckConfLog;exit 1; }


echo -n ' Restarting Shinken .......... '
restartShinken && echo $stringOk || echo $stringKo

########################################## ##########################################################
# THE END !
########################################## ##########################################################
