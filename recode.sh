#!/bin/bash

fileToRecode='./hosts.csv'
tmpFile="./tmp.$$"

mv $fileToRecode $tmpFile
iconv --from-code=ISO-8859-1 --to-code=UTF-8 $tmpFile > $fileToRecode
rm $tmpFile
