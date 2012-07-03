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
from modules import fichier

debug  = debug.Debug()


class Csv(object):

    def __init__(self, params):
        self.fileName   = params['fileName']
        self.data       = self.loadDataFromFile()
        self.currentRow	= 0


    def loadDataFromFile(self):
        csvFile = fichier.FileCsv({ 'name' : self.fileName })
#        debug.show(csvFile.loadContentIntoDict())
        csvFileContents = csvFile.loadContentIntoDict()
        self.header     = csvFile.getHeader()   # csvFile.header only exists after csvFile.loadContentIntoDict() was run
        return csvFileContents


    def setCurrentRow(self, rowId):
        self.currentRow = rowId


    def getCellFromCurrentRow(self, cellName): # TODO : except on unknown column name
        try:
            return self.data[self.currentRow][cellName]
        except KeyError:
            debug.die({ 'exitMessage' : 'No column "' + cellName + '" (CaSe SeNsItIvE !) found in "' + config.configFilesPath + config.csvFileName + "\".\nThis is usually caused by an error in a .ini file. Find files where \"" + cellName + "\" is refered to with : grep -r \"" + cellName + "\" *" })



    def currentRowHasCheckCommand(self):
        return 1 if len(str(self.data[self.currentRow][config.csvHeaderCheckCommand])) else 0


    def getCurrentRow(self):
        return self.data[self.currentRow]


    def setHostDirectives(self,params):
        self.data[self.currentRow]['hostDirectives'] = params['hostDirectives']


##    def getRawData(self):
##        csvFile = fichier.Fichier({
##                'name'  : self.fileName,
##                })
##        return csvFile.readWholeContent()


##    # TODO : allow parsing csv by row, and retrieve data as csv[rowId][columnName]
##    def getCleanData(self):
##        rawData    = self.getRawData()
##        return 0

##    def __init__(self):
##        fileCsv = fichier.FileCsv({
##            'name'  : config.csvFileName,
##            'fs'    : config.csvFileFs
##            })
##        self.data       = fileCsv.getData()
##        self.header     = fileCsv.getHeader()
##        self.currentRow	= 0
##
##
##
##
##    def getKeys(self):
##        return self.data.keys()
##
##
##    def getCurrentHostCell(self,columnName):
##        try:
##            return self.data[self.currentRow][columnName]
##        except KeyError:
##            debug.die({ 'exitMessage' : 'No column "' + columnName + '" found in "' + config.configFilesPath + config.csvFileName + "\".\nFind files where \"" + columnName + "\" is refered to with : grep -r \"" + columnName + "\" *" })
##
##
##
##
##    def getHostnameFromCurrentRow(self):
##        return self.data[self.currentRow][config.csvHeaderHostName]
##
##
##
##
##
##
##
##
    def columnExists(self,columnHeader):
        return 1 if columnHeader in self.header else 0
