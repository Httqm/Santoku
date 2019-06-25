#!/bin/bash

# Copyright (C) 2013 Matthieu FOURNET, fournet.matthieu@gmail.com
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

########################################## RUN_ME_AFTER_GIT_CLONE.sh ################################
# The files $configFile and $deploymentScript (see below) are necessary for Santoku and to deploy the
# generated configuration to Shinken. Skeleton of these files are provided with Santoku in GitHub,
# but since they must be modified locally, I don't want them to be overwritten on the next
# 'git clone'.
# This is why they are provided as 'filename$extension' (see $extension below).
#
# This script, run after 'git clone', copies the '*$extension' files into their local name so that
# they can be edited locally.
# If one of the files already exists, it won't be overwritten.
########################################## ##########################################################

extension='-dist'

configFile='./modules/config.py'
deploymentScript='./deployToShinken.sh'

for fileName in "$configFile" "$deploymentScript"; do
    [ -f "$fileName" ] || cp "$fileName$extension" "$fileName"
done
