#!/usr/bin/env python3
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
from modules import Fichier


debug = debug.Debug()


class Directives(object):

    def loadContentsOfDirectivesDotIniFile(self):
        fileIniDirectives = Fichier.FileIni(fileName = config.iniFolderGeneric + config.fileDirectivesIni)
        return fileIniDirectives.loadData()


    def compareNumberOfNamesAndValues(self, names, values, hostName, csvLineNumber):
        sameNumberOfNamesAndValues = (len(names)) == (len(values))
        if (not sameNumberOfNamesAndValues):
            debug.die(exitMessage = 'Error in source file "' + config.csvFileName + '" for host "' + hostName \
                + '" (line ' + str(csvLineNumber) + ') : columns "' \
                + config.csvHostDirectivesNames + '" and "' + config.csvHostDirectivesValues \
                + '" don\'t have the same number of parameters.'
                )


    def _getIndexOfCheckIntervalInDirectivesNames(self, directives):
        try:
            index = directives['names'].index(config.checkIntervalDirective)
        except ValueError:
            return None
        else:
            return index


    def getCheckInterval(self, directives):
        index = self._getIndexOfCheckIntervalInDirectivesNames(directives)
        try:
            return int(directives['values'][index])
        except TypeError:
            return config.defaultHostCheckInterval
