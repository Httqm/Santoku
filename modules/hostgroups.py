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


from modules import pattern
from modules import fichier
from modules import config
from modules import debug


class Hostgroups(object):

    def __init__(self):
        self.members = {} # hg name => hg members
        self.loadFileIni()
        self.loadPattern()


    def addHostToGroups(self, params):
        for hg in params['groups']:
            if not hg in self.members:  # if 'hostGroups[hg]' doesn't exist yet, create it.
                self.members[hg] = []
            self.members[hg].append(params['host'])	# then store 'host' in it !


    def loadFileIni(self):
        self.fileIni = fichier.FileIni({
            'name'  : config.configFilesPath + config.fileHostgroupIni,
            'fs'    : '',
            })
        self.fileIniData = self.fileIni.loadData()


    def loadPattern(self):
        try:
            self.hostGroupPattern = pattern.Pattern({
                'file'          : config.configFilesPath + config.fileHostgroupIni,
                'pattern'       : self.fileIniData[config.iniPatternString],
#                'variable2tag'  : self.fileIniData[config.iniVarToTagString]
                })
        except KeyError:
            debug.die({ 'exitMessage' : 'Key error  : key "' + config.iniPatternString + '" doesn\'t exist in "' + self.fileIni.name + '"' })


    def make(self):
        result = ''
        for hostgroupName in self.members:
            HG                      = {}
            members                 = ', '.join(self.members[hostgroupName])    # hosts of 'hostgroupName', as a string
            HG['hostGroupName']     = hostgroupName
            HG['hostGroupAlias']    = hostgroupName
            HG['hostGroupMembers']  = members

            result += self.hostGroupPattern.apply(HG) + "\n"

        return result
