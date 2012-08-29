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
        self.nbChecksPerHour    = 0
        self.directivesIni      = directives.loadContentsOfDirectivesDotIniFile()


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
        if(checkInterval):  # to avoid division by 0
            self.nbChecksPerHour += (minutesPerHour / float(checkInterval))


    def checkUniqueness(self):
        #debug.show(self.output)
#        myRegExp = re.compile('\{\s*host_name\s*(\w*)\s+.*?service_description\s*(\w*(\s\w*)*).*?}')
        myRegExp = re.compile('\{\s*host_name\s*(\w*)\s+.*?service_description\s*([\w\s]*?)\s{2,}.*?}')
        """
        The 'magic' in this RegExp was the 'lazy star' : .*? forcing the RegExp engine
        to match 'a series of any character that is AS SHORT AS POSSIBLE'.
        The answer was here :
            http://www.regular-expressions.info/repeat.html#greedy
        """

        import string
        singleLineOutput = string.replace(self.output, '\n', '')
        #print singleLineOutput
        match = myRegExp.findall(singleLineOutput)
        if(match):
            myList = []
            for item in match:
                matchedHostName             = item[0]
                matchedServiceDescription   = item[1]
                concatenatedHostNameAndServiceDescription = matchedHostName + matchedServiceDescription
                #print concatenatedHostNameAndServiceDescription
                if concatenatedHostNameAndServiceDescription in myList:
                    #print 'found in list'
                    debug.die({'exitMessage' : 'The service description "' + matchedServiceDescription \
                        + '" is not unique for host "' + matchedHostName + '".\nInvestigate "' \
                        + config.outputPath + config.outputFileServices + '" for details.'})
                else:
                    #print 'not in list'
                    myList.append(concatenatedHostNameAndServiceDescription)



class Service(object):

    def __init__(self, params):
        self._csv               = params['csv']
        self._csvServiceName    = params['serviceCsvName']
        self._allServices       = params['allServices']
        self._cleanName         = self._csvServiceName.replace(config.csvHeaderFs + config.csvHeaderDo,'')
        self._iniFileName       = config.iniFolderPlugins + self._cleanName + '.ini'
        self._loadIniFiles()
        self._loadPatterns()


    def _loadIniFiles(self):
        self._directivesIni = self._allServices.directivesIni
        self._loadPluginIniFile()


    def _loadPluginIniFile(self):
        self._fileIni       = FileIni({'name': self._iniFileName})
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
                + '" in config file "' + self._fileIni.name + '"'})


    def _loadPatterns(self):
        self._patternService = pattern.Pattern({
            'file'      : self._iniFileName,
            'pattern'   : self._fileIniData[config.iniPatternString]
            })
        self._patternDirectives = pattern.Pattern({
            'file'      : config.iniFolderGeneric + config.fileDirectivesIni,
            'pattern'   : self._directivesIni[config.iniPatternString]
            })


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
        serviceData     = {}

        # Parsing data stored in dict to register as many services as the number of values in multi-valued cells
        maxRounds       = 1
        currentRound    = 0

        while currentRound < maxRounds:
            serviceData[currentRound] = {
                config.csvHeaderHostName    : params['hostName'],
                config.csvHeaderUse         : config.csvGenericService
                }
            for serviceField in serviceCsvData:
                valuesOfMultiValuedCell = serviceCsvData[serviceField].split(config.csvMultiValuedCellFS)

                # Excluding the service directives columns here to avoid duplicating the service definition
                if(not self._isAServiceDirectiveField(serviceField)):
                    maxRounds = len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds
                    # TODO : this is ugly ! -----^

                try:
                    tmpValue = valuesOfMultiValuedCell[currentRound]
                except IndexError:
                    tmpValue = valuesOfMultiValuedCell[0]

                serviceData[currentRound][serviceField] = tmpValue

            currentRound += 1

        self._result = {'serviceData': serviceData, 'maxRounds': maxRounds}


    def _isAServiceDirectiveField(self, fieldName):
        return ((config.csvServiceDirectivesNames == fieldName) or (config.csvServiceDirectivesValues == fieldName))


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
            tmp += self._patternService.apply(self._result['serviceData'][i]) + "\n"
            self._allServices.count()
            self._allServices.countChecksPerHour(self.getCheckInterval())
        return tmp


    def loadDirectivesFromCsvData(self):
        self._directivesCsv = {
            'names'  : self._csv.getCellFromCurrentRow(self._csvColumnHavingServiceDirectivesNames).split(config.csvMultiValuedCellFS),
            'values' : self._csv.getCellFromCurrentRow(self._csvColumnHavingServiceDirectivesValues).split(config.csvMultiValuedCellFS)
            }


    def applyServiceDirectivesPattern(self):
        self.serviceDirectives = ''
        for name, value in enumerate(self._directivesCsv['names']):
            self.serviceDirectives += self._patternDirectives.apply({
                'directiveName'     : self._directivesCsv['names'][name],
                'directiveValue'    : self._directivesCsv['values'][name]
                })
        return self.serviceDirectives


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
            return directives.getCheckInterval(self._directivesCsv)
        else:
            return config.defaultHostCheckInterval
