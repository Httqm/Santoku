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
from modules import controller

controller  = controller.Controller()


class Csv(object):

    def __init__(self):
        fileCsv = fichier.FileCsv({
            'name'  : config.csvFileName,
            'fs'    : config.csvFileFs
            })
        self.data       = fileCsv.getData()
        self.header     = fileCsv.getHeader()
        self.currentRow	= 0


    def setCurrentRow(self,params):
        self.currentRow = params['rowId']


    def getKeys(self):
        return self.data.keys()


    def getCell(self,columnName):
        try:
            return self.data[self.currentRow][columnName]
        except KeyError:
            controller.die({ 'exitMessage' : 'No column "' + columnName + '" found in "' + config.configFilesPath + config.csvFileName + "\".\nFind files where \"" + columnName + "\" is refered to with : grep -r \"" + columnName + "\" *" })


    def getCurrentRow(self):
        return self.data[self.currentRow]


    def getHostnameFromCurrentRow(self):
        return self.data[self.currentRow][config.csvHeaderHostName]


    def currentRowHasCheckCommand(self):
        return 1 if len(str(self.data[self.currentRow][config.csvHeaderCheckCommand])) else 0


    def setHostDirectives(self,params):
        self.data[self.currentRow]['hostDirectives'] = params['hostDirectives']


    def getHeader(self):
        return self.header


    def columnExists(self,columnHeader):
        return 1 if columnHeader in self.header else 0

