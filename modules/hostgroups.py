#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


from modules import pattern
from modules import fichier
from modules import config
from modules import debug


class Hostgroups(object):

    def __init__(self):
        self._hostGroupToMembers = {}  # dict : {'hostGroupName': listOfMembers}
        self._loadFileIni()
        self._loadPattern()


    def addHostToGroups(self, host, groups):
        for group in groups:
            if not group in self._hostGroupToMembers:                   # if 'hostGroups[group]' doesn't exist yet, create it.
                self._hostGroupToMembers[group] = []
            if host not in self._hostGroupToMembers[group]:
                self._hostGroupToMembers[group].append(host)  # then store 'host' in it (unless it's already there)


    def _loadFileIni(self):
        self._fileIni       = fichier.FileIni(fileName = config.iniFolderGeneric + config.fileHostgroupIni)
        self._fileIniData   = self._fileIni.loadData()


    def _loadPattern(self):
        try:
            self._hostGroupPattern = pattern.Pattern(
                fileName    = config.iniFolderGeneric + config.fileHostgroupIni,
                pattern     = self._fileIniData[config.iniPatternString]
                )
        except KeyError:
            debug.die(exitMessage = 'Key error  : key "' + config.iniPatternString + '" doesn\'t exist in "' + self._fileIni.name + '"')


    def make(self):
        result = ''
        for hostgroupName in self._hostGroupToMembers:
            theHostGroup                        = {}
            theMembers                          = ', '.join(self._hostGroupToMembers[hostgroupName])    # hosts of 'hostgroupName', as a string
            theHostGroup['hostGroupName']       = hostgroupName
            theHostGroup['hostGroupAlias']      = hostgroupName
            theHostGroup['hostGroupMembers']    = theMembers

            result += self._hostGroupPattern.apply(theHostGroup) + "\n"

        return result
