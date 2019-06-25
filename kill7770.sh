#!/bin/bash

######################################### kill7770.sh ###############################################
# Sometimes, the Python process listening on port 7770 doesn't stop when required to do so. (WHY ???)
# Thus, Shinken can not restart since there's already someone listening on port 7770.
# 
# This script is to automate the killing of this process.
######################################### ###########################################################

pidOfPythonProcessListeningOnPort7770=$(netstat -laputen | grep ":7770" | awk '{ print $9}' | cut -d '/' -f 1);

[ -n "$pidOfPythonProcessListeningOnPort7770" -a -d "/proc/$pidOfPythonProcessListeningOnPort7770" ] && {
	echo -n "Killing PID '$pidOfPythonProcessListeningOnPort7770' ... "
	kill -1 "$pidOfPythonProcessListeningOnPort7770" && echo 'OK' || echo 'KO';
	} || echo 'No PID to kill.'
