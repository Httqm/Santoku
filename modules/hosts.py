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
from modules import fichier
from modules import pattern
from modules import debug


debug = debug.Debug()


class AllHosts(object):

    def __init__(self):
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
        self._loadDirectives()


    def _loadIniFile(self):
        fileIniHost         = fichier.FileIni({ 'name': config.configFilesPath + config.fileHostIni })
        self._iniFileData   = fileIniHost.loadData()
#        self.checkIniFile()	# TODO


    def _loadDirectives(self):
        fileIniDirectives   = fichier.FileIni({ 'name': config.configFilesPath + config.fileDirectivesIni })
        self._directives    = fileIniDirectives.loadData()


    # TODO : fix this : loadPatterns is private, but self.pattern* below seem to be public :-(
    def _loadPatterns(self):
        self.patternHost = pattern.Pattern({
            'file'          : config.configFilesPath + config.fileHostIni,
            'pattern'       : self._iniFileData[config.iniPatternString],
            })
        self.patternDirectives = pattern.Pattern({
            'file'          : config.configFilesPath + config.fileDirectivesIni,
            'pattern'       : self._directives[config.iniPatternString],
            })


    def clean(self):
        self._removeDirectivesHavingNoValue()


    def _removeDirectivesHavingNoValue(self):
        directivesList = ['check_command']
        #re.sub(pattern, repl, string, count=0, flags=0)
        #self.output = re.sub('^\s*check_command\s*$', '', self.output)
        for directive in directivesList:
            self.output = re.sub(r'\s+' + directive + '\s+\n', r'\n', self.output)
#        debug.show(self.output)


##    def checkIniFile(self):
##        self.searchPatternStanza()
##        self.searchVariablesStanza()
##
##
##    # TODO : duplicate code below !!!!!
##    def searchPatternStanza(self):
##        try:
##            self._iniFileData[config.iniPatternString]
##        except KeyError:
##            debug.die({ 'exitMessage' : 'Key error  : key "' + config.iniPatternString + '" not found in "' + self.fileIniHost.name})
##
##
##    def searchVariablesStanza(self):
##        try:
##            self._iniFileData[config.iniVarToTagString]
##        except KeyError:
##            debug.die({ 'exitMessage' : 'Key error  : key "' + config.iniVarToTagString + '" not found in "' + self.fileIniHost.name})
##    # /TODO


class Host(object):
    def __init__(self, params):
        self._csv        = params['csv']
        self._allHosts   = params['allHosts']


    def isMarkedToBeIgnored(self):
#        debug.show(self._csv.getCellFromCurrentRow('host_name'))
        return 1 if self._csv.getCellFromCurrentRow(config.csvHeaderIgnoreHost) == '1' else 0


    def isAlreadyRegisteredInHostsCfg(self):
        """
        A host may appear on several lines of the source CSV file.
        This is especially true with 'virtual' hosts that are not attached to a physical machine.
        Such hosts are then called 'duplicated'.
        As a host_name may also appear as a parent, we only try to match the specified host_name
        with all the known host_names.
        """
        import re
        match = re.search(config.csvHeaderHostName \
            + '\s*' \
            + self._csv.getCellFromCurrentRow(config.csvHeaderHostName) \
            , self._allHosts.output)
#        if match:
#            debug.show(self._csv.getCellFromCurrentRow(config.csvHeaderHostName)+' IS DUPLICATED')
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


    def loadDirectives(self):   # TODO : should this be public ?
        self._checkCsvHostDirectivesExist()
        directives          = ''
        directivesNames     = self._csv.getCellFromCurrentRow(config.csvHostDirectivesNames).split(config.csvMultiValuedCellFS)
        directivesValues    = self._csv.getCellFromCurrentRow(config.csvHostDirectivesValues).split(config.csvMultiValuedCellFS)

        for index,value in enumerate(directivesNames):
            directives += self._allHosts.patternDirectives.apply({ 'directiveName': directivesNames[index], 'directiveValue' : directivesValues[index]})
        return directives


    def _checkCsvHostDirectivesExist(self):
        self._searchCsvHostDirectivesNames()
        self._searchCsvHostDirectivesValues()


    def _searchCsvHostDirectivesNames(self):
        try:
            self._csv.getCellFromCurrentRow(config.csvHostDirectivesNames)
        except KeyError:
            debug.die({ 'exitMessage': 'Key error : key "' + config.csvHostDirectivesNames + '" not found in "' + config.csvFileName + '"'})


    def _searchCsvHostDirectivesValues(self):
        try:
            self._csv.getCellFromCurrentRow(config.csvHostDirectivesValues)
        except KeyError:
            debug.die({ 'exitMessage': 'Key error : key "' + config.csvHostDirectivesValues + '" not found in "' + config.csvFileName + '"'})


    def getCheckCommand(self):
        checkCommandName = self._csv.getCellFromCurrentRow(config.csvHeaderCheckCommand)
        hostCheckFileIni = fichier.FileIni({ 'name': config.configFilesPath + checkCommandName + '.ini' })
        hostCheckFileIni.loadData()
        return {
            'serviceName'       : checkCommandName,
            'serviceCommand'    : hostCheckFileIni.loadData()['COMMAND']	# TODO : hardcoded keyword /!\
            }
