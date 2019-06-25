#!/usr/bin/env bash

fileToRecode='./hosts.csv'
tmpFile=$(mktemp)

mv "$fileToRecode" "$tmpFile"
iconv --from-code=ISO-8859-1 --to-code=UTF-8 "$tmpFile" > "$fileToRecode"
rm "$tmpFile"
