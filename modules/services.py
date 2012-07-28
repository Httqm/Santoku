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
from modules import debug
from modules import directives
from modules import fichier
from modules import pattern
import re


debug       = debug.Debug()
directives  = directives.Directives()
FileIni     = fichier.FileIni
Pattern     = pattern.Pattern


class AllServices(object):

    def __init__(self):
        self.output = ''
        self.number = 0
        self.nbChecksPerHour = 0


    def getList(self, csvHeaders):
        self._list = []
        for field in csvHeaders:
            match = re.search('.*' + config.csvHeaderFs + config.csvHeaderDo + '$', field)
            if(match):
                self._list.append(field)
        return self._list


    def count(self):
        self.number += 1


    def countChecksPerHour(self, checkInterval):
        minutesPerHour = 60
        if(checkInterval):  # avoid division by 0
            self.nbChecksPerHour += (minutesPerHour / float(checkInterval))
#        debug.show('nb checks so far = ' + str(self.nbChecksPerHour))


class Service(object):

    def __init__(self, params):
        self._csv               = params['csv']
        self._csvServiceName    = params['serviceCsvName']
        self._allServices       = params['allServices']
        self._cleanName         = self._csvServiceName.replace(config.csvHeaderFs + config.csvHeaderDo,'')
        self._iniFileName       = config.configFilesPath + self._cleanName + '.ini'
        self._loadIniFiles()
        self._loadPatterns()


    def _loadIniFiles(self):
        self._loadIniFile()
#        self._loadContentsOfDirectivesDotIniFile()
	self._directives = directives.loadContentsOfDirectivesDotIniFile()
        # TODO : this is repeated for every service. Once is enough. fix it !


    def _loadIniFile(self):
        self._fileIni       = FileIni({ 'name': self._iniFileName })
        self._fileIniData   = self._fileIni.loadData()
        self._checkFileIni()


    def _checkFileIni(self):
        self._fileIni.searchSection(config.iniPatternString)
        self._fileIni.searchSection(config.iniCommandString)
        self._checkFileIniCommandNamesMatch()


    def getCommand(self):
        try:
            return {
                'serviceName'       : self._cleanName,
                'serviceCommand'    : self._fileIniData[config.iniCommandString]
                }
        except KeyError:
            debug.die({'exitMessage': 'No command specified for service "' + self._cleanName \
                + '" in config file "' + self._fileIni.name + '"' })


    def _loadPatterns(self):
        self._patternService = pattern.Pattern({
            'file'      : self._iniFileName,
            'pattern'   : self._fileIniData[config.iniPatternString],
            })
        self._patternDirectives = pattern.Pattern({
            'file'      : config.configFilesPath + config.fileDirectivesIni,
            'pattern'   : self._directives[config.iniPatternString],
            })


#    def _loadContentsOfDirectivesDotIniFile(self):
#        fileDirectivesIni       = FileIni({ 'name': config.configFilesPath + config.fileDirectivesIni })
#        self._directives = fileDirectivesIni.loadData()
#        debug.show(self._directives)
#        debug.show(config.configFilesPath + config.fileDirectivesIni)


    def isEnabled(self):
        return 1 if self._csv.getCellFromCurrentRow(self._csvServiceName) == '1' else 0


    def getName(self):
        return self._cleanName


    def hasDirectives(self):
        self._hasDirectives = 1
        self._csvColumnHavingServiceDirectivesNames    = self._cleanName + config.csvHeaderFs + config.csvServiceDirectivesNames
        self._csvColumnHavingServiceDirectivesValues   = self._cleanName + config.csvHeaderFs + config.csvServiceDirectivesValues
        for columnName in [self._csvColumnHavingServiceDirectivesNames, self._csvColumnHavingServiceDirectivesValues]:
            if(self._csv.columnExists(columnName)):
                self._hasDirectives = self._hasDirectives and self._csv.getCellFromCurrentRow(columnName)
            else:
                self._hasDirectives = 0
        return self._hasDirectives


    def buildArrayOfServices(self, params):
        """
        Return an associative array containing all service(s) data ready to be injected into pattern.
        This method handles multi-valued CSV cells
        """
        serviceCsvData  = self._loadServiceData(params)
        champsValeurs   = {}

        # Parsing data stored in dict to register as many services as the number of values in multi-valued cells
        maxRounds       = 1
        currentRound    = 0

        while currentRound < maxRounds:
            champsValeurs[currentRound]	= {
                config.csvHeaderHostName    : params['hostName'],
                config.csvHeaderUse         : config.csvGenericService
                }
            for serviceField in serviceCsvData:
                valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(config.csvMultiValuedCellFS)

                # Excluding the service directives columns here to avoid duplicating the service definition
                if((serviceField != config.csvServiceDirectivesNames) and (serviceField != config.csvServiceDirectivesValues)):
                    maxRounds = len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds

                try:
                    tmpValue = valuesOfMultiValuedCell[currentRound]
                except IndexError:
                    tmpValue = valuesOfMultiValuedCell[0]

                champsValeurs[currentRound][serviceField] = tmpValue

            currentRound += 1

        self._result	= { 'champsValeurs': champsValeurs, 'maxRounds': maxRounds }


    def _loadServiceData(self, params):
        """
        For the current host and the current service, return :
        - 'clean' CSV header lines (without the 'serviceName:')
        - cell values (including multiple values and field separators if any)
        """
        serviceCsvData = {}

        # storing CSV data in a dict to play with it later
        for field in self._csv.header:
            match = re.search(self._cleanName + config.csvHeaderFs + '.*', field)
            if(match):
                # parsing all CSV columns related to this service
                serviceCsvData[field.replace(self._cleanName + config.csvHeaderFs, '')] = params['csvDataLine'][field]

        # appending 'serviceDirectives'
        # serviceCsvData contains 2 useless keys : 'serviceDirectivesNames' and 'serviceDirectivesValues'
        serviceCsvData['serviceDirectives'] = params['serviceDirectives']

        return serviceCsvData


    def make(self):
        tmp = ''    # must be an empty string to allow '+=' below
        for i in range(self._result['maxRounds']):
            tmp += self._patternService.apply(self._result['champsValeurs'][i]) + "\n"
            self._allServices.count()
        return tmp


    def loadDirectivesFromCsvData(self):
        self._directives	= {
            'names'  : self._csv.getCellFromCurrentRow(self._csvColumnHavingServiceDirectivesNames).split(config.csvMultiValuedCellFS),
            'values' : self._csv.getCellFromCurrentRow(self._csvColumnHavingServiceDirectivesValues).split(config.csvMultiValuedCellFS)
            }


    def applyServiceDirectivesPattern(self):
        self.serviceDirectives = ''
        for name, value in enumerate(self._directives['names']):
            self.serviceDirectives += self._patternDirectives.apply({
                'directiveName'     : self._directives['names'][name],
                'directiveValue'    : self._directives['values'][name]
                })
        return self.serviceDirectives


##    def _checkFileIniBothTagSurroundingCharsAreThere(self):
##        for sectionTitle in self._fileIniData:
##            match = re.search('(("|\s)\$[a-zA-Z_:]*("|\s|/))|(("|\s)[a-zA-Z_:]*\$("|\s|/))', str(self._fileIniData[sectionTitle]))
##            if(match):
##                debug.die({ 'exitMessage' : 'Missing leading/trailing "$" in expression "' + match.group(0) + '" in the "[' + sectionTitle + ']" section of "' + self._fileIni.name + '"'})


    def _checkFileIniCommandNamesMatch(self):
        commandInPatternSection = self._getCommandValueFromSection({
            'directive'     : config.commandDirectiveInServiceDefinition,
            'sectionTitle'  : config.iniPatternString
            })

        commandInCommandSection = self._getCommandValueFromSection({
            'directive'     : config.commandDirectiveInCommandDefinition,
            'sectionTitle'  : config.iniCommandString
            })

        if commandInPatternSection != commandInCommandSection:
            debug.die({'exitMessage': 'Commands don\'t match between the "' \
                + config.iniPatternString + '" (' + config.commandDirectiveInServiceDefinition \
                + ' ' + commandInPatternSection + ') and the "' + config.iniCommandString \
                + '" (' + config.commandDirectiveInCommandDefinition + ' ' \
                + commandInCommandSection + ') sections of config file "' + self._iniFileName + '"'
                })


    def _getCommandValueFromSection(self, params):
        match = re.search('\s' + params['directive'] + '\s + (\w*)', self._fileIniData[params['sectionTitle']])
        if match:
            return match.group(1)
        else:
            debug.die({'exitMessage': '"' + params['directive'] + '" directive not found in "' \
                + params['sectionTitle'] + '" section of config file "' + self._iniFileName + '"'
                })


    def getCheckInterval(self):
        if self._hasDirectives:
            return directives.getCheckInterval(self._directives)
        else:
            return config.defaultHostCheckInterval

