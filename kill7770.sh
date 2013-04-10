#!/bin/bash

######################################### kill7770.sh ###############################################
# Sometimes, the Python process listening on port 7770 doesn't stop when required to do so.
# Thus, Shinken can not restart since there's already someone listening on port 7770.
# 
# This script is to automate the killing of this process
######################################### ###########################################################

python7770Pid=$(netstat -laputen | grep ":7770" | awk '{ print $9}' | cut -d '/' -f 1);
#echo $python7770Pid;
[ "$python7770Pid" != "" -a -d "/proc/$python7770Pid" ] && {
	echo -n "Killing PID $python7770Pid ... "
	kill -1 $python7770Pid && echo 'OK' || echo 'KO';
	} || echo 'No PID to kill.'