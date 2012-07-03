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


from modules import config
from modules import fichier
from modules import pattern
from modules import debug

debug = debug.Debug()


class AllHosts(object):

    def __init__(self):
        self.loadIniFiles()
        self.loadPatterns()
        self.output = ''
        self.number = {
            'valid'         : 0,
            'ignored'       : 0,
            'duplicated'    : 0
            }


    def incrementCountOf(self,hostType):
        self.number[hostType] += 1


    def loadIniFiles(self):
        self.loadIniFile()
        self.loadDirectives()


    def loadIniFile(self):
        fileIniHost = fichier.FileIni({
            'name'  : config.configFilesPath + config.fileHostIni,
#            'fs'    : '',
            })
        self.iniFileData = fileIniHost.loadData()
#        self.checkIniFile()	# TODO


    def loadDirectives(self):
        fileIniDirectives = fichier.FileIni({
            'name'  : config.configFilesPath + config.fileDirectivesIni,
#            'fs'    : '',
            })
        self.directives = fileIniDirectives.loadData()
#        debug.show(self.directives)


    def loadPatterns(self):
#        debug.show(config.configFilesPath + config.fileHostIni)
#        debug.show(self.iniFileData[config.iniPatternString])
        self.patternHost = pattern.Pattern({
            'file'          : config.configFilesPath + config.fileHostIni,
            'pattern'       : self.iniFileData[config.iniPatternString],
#            'variable2tag'  : self.iniFileData[config.iniVarToTagString]   # remove this
            })
#        debug.show(self.patternHost)
        self.patternDirectives = pattern.Pattern({
            'file'          : config.configFilesPath + config.fileDirectivesIni,
            'pattern'       : self.directives[config.iniPatternString],
#            'variable2tag'  : self.directives[config.iniVarToTagString]
            })




##    def checkIniFile(self):
##        self.searchPatternStanza()
##        self.searchVariablesStanza()
##
##
##    # TODO : duplicate code below !!!!!
##    def searchPatternStanza(self):
##        try:
##            self.iniFileData[config.iniPatternString]
##        except KeyError:
##            controller.die({ 'exitMessage' : 'Key error  : key "' + config.iniPatternString + '" not found in "' + self.fileIniHost.name})
##
##
##    def searchVariablesStanza(self):
##        try:
##            self.iniFileData[config.iniVarToTagString]
##        except KeyError:
##            controller.die({ 'exitMessage' : 'Key error  : key "' + config.iniVarToTagString + '" not found in "' + self.fileIniHost.name})
##    # /TODO


class Host(object):
    def __init__(self,params):
        self.csv        = params['csv']
##        self.pattern    = {}
        self.allHosts   = params['allHosts']

        return


    def isMarkedToBeIgnored(self):
        return 1 if self.csv.getCellFromCurrentRow(config.csvHeaderIgnoreHost) == '1' else 0


    def isDuplicated(self):
        """
        A host may appear on several lines of the source CSV file.
        This is especially true with 'virtual' hosts that are not attached to a physical machine.
        Such hosts are then called 'duplicated'.
        """
        import re
        match = re.search(self.csv.getCellFromCurrentRow(config.csvHeaderHostName), self.allHosts.output)
        return 1 if match else 0


    def buildTagValues(self):
        tags = self.allHosts.patternHost.searchTags()
        self.tagsAndValues = {}
        for tag in tags:
            self.tagsAndValues[tag] = self.csv.getCellFromCurrentRow(tag)
#        debug.show('tag values : ' + str(self.tagsAndValues))


    def applyHostPattern(self):
        self.buildTagValues()
        return self.allHosts.patternHost.apply(self.tagsAndValues) + "\n"


    def loadHostGroupsFromCsv(self):
        return self.csv.getCellFromCurrentRow(config.csvHeaderHostgroups).split(config.csvMultiValuedCellFS)


    def loadDirectives(self):
        self.checkCsvHostDirectivesExist()
        directives          = ''
        directivesNames     = self.csv.getCellFromCurrentRow(config.csvHostDirectivesNames).split(config.csvMultiValuedCellFS)
        directivesValues    = self.csv.getCellFromCurrentRow(config.csvHostDirectivesValues).split(config.csvMultiValuedCellFS)

#        debug.show(directivesNames)
#        debug.show(directivesValues)
        for index,value in enumerate(directivesNames):
#            debug.show('LOAD DIRECTIVES : '+str(index)+' '+value)
            directives += self.allHosts.patternDirectives.apply({ 'directiveName' : directivesNames[index], 'directiveValue' : directivesValues[index]})
#        debug.show(directives)
        return directives


    def checkCsvHostDirectivesExist(self):
        self.searchCsvHostDirectivesNames()
        self.searchCsvHostDirectivesValues()


    def searchCsvHostDirectivesNames(self):
        try:
            self.csv.getCellFromCurrentRow(config.csvHostDirectivesNames)
        except KeyError:
            controller.die({ 'exitMessage' : 'Key error : key "' + config.csvHostDirectivesNames + '" not found in "' + config.csvFileName + '"'})


    def searchCsvHostDirectivesValues(self):
        try:
            self.csv.getCellFromCurrentRow(config.csvHostDirectivesValues)
        except KeyError:
            controller.die({ 'exitMessage' : 'Key error : key "' + config.csvHostDirectivesValues + '" not found in "' + config.csvFileName + '"'})


    def getCheckCommand(self):
        checkCommandName = self.csv.getCellFromCurrentRow(config.csvHeaderCheckCommand)
        hostCheckFileIni = fichier.FileIni({
            'name'  : config.configFilesPath + checkCommandName + '.ini',
            })
        hostCheckFileIni.loadData()

        return {
            'serviceName'       : checkCommandName,
            'serviceCommand'    : hostCheckFileIni.loadData()['COMMAND']
            }
