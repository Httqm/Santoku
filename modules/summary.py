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


from modules import pattern
from modules import fichier
from modules import config
from modules import debug

debug = debug.Debug()


class Summary(object):

    def __init__(self):
        self._loadFileIni()
        self._loadPattern()


    def _loadFileIni(self):
        self._fileIni       = fichier.FileIni({'name': config.configFilesPath + config.fileSummaryIni})
        self._fileIniData   = self._fileIni.loadData()


    def _loadPattern(self):
        try:
            self._summaryPattern = pattern.Pattern({
                'file'      : config.configFilesPath + config.fileSummaryIni,
                'pattern'   : self._fileIniData[config.iniPatternString],
                })
        except KeyError:
            debug.die({'exitMessage': 'Key error  : key "' + config.iniPatternString + '" doesn\'t exist in "' + self._fileIni.name + '"'})


    def make(self, params):
        return self._summaryPattern.apply({
            'nbLines'           : params['nbLines'],
            'fileCsv'           : config.configFilesPath + config.csvFileName,
            'fileHosts'         : config.outputPath + config.outputFileHosts,
            'fileServices'      : config.outputPath + config.outputFileServices,
            'fileCommands'      : config.outputPath + config.outputFileCommands,
            'nbHostsTotal'      : params['hostsTotal'],
            'nbHostsValid'      : params['hostsValid'],
            'nbHostsIgnored'    : params['hostsIgnored'],
            'nbHostsDuplicated' : params['hostsDuplicated'],
            'nbServicesTotal'   : params['servicesTotal'],
            'nbCommandsTotal'   : params['commandsTotal'],
            })
