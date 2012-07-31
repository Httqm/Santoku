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


debug = debug.Debug()


class Directives(object):

#    def __init__(self):
#        self.compteurALC=0


    def loadContentsOfDirectivesDotIniFile(self):
        fileIniDirectives   = fichier.FileIni({'name': config.configFilesPath + config.fileDirectivesIni})
#        # DEBUG !!!
#        self.compteurALC+=1
#        debug.show(self.compteurALC)
#        # /DEBUG !!!
        return fileIniDirectives.loadData()


    def compareNumberOfNamesAndValues(self, params):
        sameNumberOfNamesAndValues = (len(params['names'])) == (len(params['values']))
        if (not sameNumberOfNamesAndValues):
            debug.die({'exitMessage': 'Error in source file "' + config.csvFileName + '" for host "' + params['hostName'] \
                + '" (line ' + str(params['csvLineNumber']) + ') : columns "' \
                + config.csvHostDirectivesNames + '" and "' + config.csvHostDirectivesValues \
                + '" don\'t have the same number of parameters.'
                })


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
