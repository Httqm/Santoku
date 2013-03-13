#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


from modules import config
from modules import debug
from modules import fichier

debug  = debug.Debug()


class Csv(object):

    def __init__(self, fileName):
        self._fileName      = fileName
        self.data           = self._loadDataFromFile()
        self._checkAllColumnHeadersAreUnique()
        self._currentRow    = 0
        self.nbLines        = 0


    def _loadDataFromFile(self):
        csvFile         = fichier.FileCsv(fileName = self._fileName)
        csvFileContents = csvFile.contents
        self.header     = csvFile.getHeader()
        return csvFileContents


    def _checkAllColumnHeadersAreUnique(self):
        knownHeaders = []
        for header in self.header:
            if header in knownHeaders:
                debug.die(exitMessage = 'The column "' + header + '" appears twice in the CSV file "' \
                    + config.csvFileName + '"')
            else:
                knownHeaders.append(header)
            

    def setCurrentRow(self, rowId):
        self._currentRow    = rowId
        self.nbLines        += 1


    def getCellFromCurrentRow(self, cellName):
        try:
            return self.data[self._currentRow][cellName]
        except KeyError:
            debug.die(exitMessage = 'No column "' + cellName + '" (CaSe SeNsItIvE !) found in "' \
                + config.csvFileName + "\".\nThis is either caused by : \n" \
                + " - wrong column name in the CSV file\n" \
                + ' - OR by an error in a .ini file. Find files where \"' + cellName + "\" is refered to with : grep -r \"" \
                + cellName + "\" *"
                )


    def currentRowHasCheckCommand(self):
        try:
            return 1 if len(str(self.data[self._currentRow][config.csvHeaderCheckCommand])) else 0
        except KeyError:
            debug.die(exitMessage = 'No column "' + config.csvHeaderCheckCommand + '" found in "' \
                + config.configFilesPath + config.csvFileName + "\".")


    def getCurrentRow(self):
        return self.data[self._currentRow]


    def setHostDirectives(self, hostDirectives):
        self.data[self._currentRow]['hostDirectives'] = hostDirectives


    def columnExists(self, columnHeader):
        return 1 if columnHeader in self.header else 0
