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


import re
from modules import config
from modules import directives
from modules import debug
from modules import fichier
from modules import pattern


debug       = debug.Debug()
directives  = directives.Directives()


class AllHosts(object):

    def __init__(self):
        self._directives = directives.loadContentsOfDirectivesDotIniFile()
        self._loadIniFiles()
        self._loadPatterns()
        self.output = ''
        self.number = {
            'valid'         : 0,
            'ignored'       : 0,
            'duplicated'    : 0
            }


    def incrementCountOf(self, hostType):
        self.number[hostType] += 1


    def _loadIniFiles(self):
        self._loadIniFile()


    def _loadIniFile(self):
        self._fileIniHost   = fichier.FileIni(fileName = config.iniFolderGeneric + config.fileHostIni)
        self._iniFileData   = self._fileIniHost.loadData()
        self.checkIniFile()


    def _loadPatterns(self):
        self.patternHost = pattern.Pattern({
            'file'      : config.iniFolderGeneric + config.fileHostIni,
            'pattern'   : self._iniFileData[config.iniPatternString],
            })
        self.patternDirectives = pattern.Pattern({
            'file'      : config.iniFolderGeneric + config.fileDirectivesIni,
            'pattern'   : self._directives[config.iniPatternString],
            })


    def clean(self):
        self._removeDirectivesHavingNoValue()


    def _removeDirectivesHavingNoValue(self):
        directivesList = [
            config.csvHeaderCheckCommand,
            config.csvHeaderParents,
            '_SSHLOGIN' # /!\ hardcoded stuff. "_SSHLOGIN" is defined in config/host.ini
            ]
        for directive in directivesList:
            self.output = re.sub(r'\s+' + directive + '\s+\n', r'\n', self.output)


    def checkIniFile(self):
        self._fileIniHost.searchSection(config.iniPatternString)



class Host(object):
    def __init__(self, params):
        self._csv        = params['csv']
        self._allHosts   = params['allHosts']


    def isMarkedToBeIgnored(self):
        return 1 if self._csv.getCellFromCurrentRow(config.csvHeaderIgnoreHost) == '1' else 0


    def isAlreadyRegisteredInHostsCfg(self):
        """
        A host may appear on several lines of the source CSV file.
        This is especially true with 'virtual' hosts that are not attached to a physical machine.
        Such hosts are then called 'duplicated'.
        As a host_name may also appear as a parent, we only try to match the specified host_name
        with all the known host_names.
        """
        match = re.search(config.csvHeaderHostName \
            + '\s*' \
            + self._csv.getCellFromCurrentRow(config.csvHeaderHostName) \
            , self._allHosts.output)
        return 1 if match else 0


    def _buildTagValues(self):
        tags                = self._allHosts.patternHost.searchTags()
        self._tagsAndValues = {}
        for tag in tags:
            self._tagsAndValues[tag] = self._csv.getCellFromCurrentRow(tag)


    def applyHostPattern(self):
        self._buildTagValues()
        return self._allHosts.patternHost.apply(self._tagsAndValues) + "\n"


    def loadHostGroupsFromCsv(self):
        return self._csv.getCellFromCurrentRow(config.csvHeaderHostgroups).split(config.csvMultiValuedCellFS)


    def loadDirectives(self):
        self._checkCsvHostDirectivesExist()
        self._directives          = ''
        self._directivesNames     = self._csv.getCellFromCurrentRow(config.csvHostDirectivesNames).split(config.csvMultiValuedCellFS)
        self._directivesValues    = self._csv.getCellFromCurrentRow(config.csvHostDirectivesValues).split(config.csvMultiValuedCellFS)

        directives.compareNumberOfNamesAndValues(
                names           = self._directivesNames,
                values          = self._directivesValues,
                hostName        = self._csv.getCellFromCurrentRow(config.csvHeaderHostName),
                csvLineNumber   = self._csv.nbLines + 1
                )

        for index,value in enumerate(self._directivesNames):
            self._directives += self._allHosts.patternDirectives.apply({
                'directiveName'     : self._directivesNames[index],
                'directiveValue'    : self._directivesValues[index]
                })
        return self._directives


    def _checkCsvHostDirectivesExist(self):
        self._searchCsvHostDirectivesNames()
        self._searchCsvHostDirectivesValues()


    def _searchCsvHostDirectivesNames(self):
        try:
            self._csv.getCellFromCurrentRow(config.csvHostDirectivesNames)
        except KeyError:
            debug.die(exitMessage = 'Key error : key "' + config.csvHostDirectivesNames + '" not found in "' + config.csvFileName + '"')


    def _searchCsvHostDirectivesValues(self):
        try:
            self._csv.getCellFromCurrentRow(config.csvHostDirectivesValues)
        except KeyError:
            debug.die(exitMessage = 'Key error : key "' + config.csvHostDirectivesValues + '" not found in "' + config.csvFileName + '"')


    def getCheckCommand(self):
        checkCommandName = self._csv.getCellFromCurrentRow(config.csvHeaderCheckCommand)
        hostCheckFileIni = fichier.FileIni(fileName = config.iniFolderPlugins + checkCommandName + '.ini')
        hostCheckFileIni.loadData()
        return {
            'serviceName'       : checkCommandName,
            'serviceCommand'    : hostCheckFileIni.loadData()[config.iniCommandString]
            }


    def getCheckInterval(self):
        self._directives = {
            'names'     : self._directivesNames,
            'values'    : self._directivesValues
            }
        return directives.getCheckInterval(self._directives)
