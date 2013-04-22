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
        self._fileIni       = fichier.FileIni(fileName = config.iniFolderGeneric + config.fileSummaryIni)
        self._fileIniData   = self._fileIni.loadData()


    def _loadPattern(self):
        try:
            self._summaryPattern = pattern.Pattern(
                fileName    = config.iniFolderGeneric + config.fileSummaryIni,
                pattern     = self._fileIniData[config.iniPatternString]
                )
        except KeyError:
            debug.die(exitMessage = 'Key error  : key "' + config.iniPatternString + '" doesn\'t exist in "' + self._fileIni.name + '"')


    def make(self, summaryData):
        return self._summaryPattern.apply({
            'nbLines'           : summaryData['nbLines'],
            'fileCsv'           : config.csvFileName,
            'fileHosts'         : config.outputPath + config.outputFileHosts,
            'fileServices'      : config.outputPath + config.outputFileServices,
            'fileCommands'      : config.outputPath + config.outputFileCommands,
            'nbHostsTotal'      : summaryData['hostsTotal'],
            'nbHostsValid'      : summaryData['hostsValid'],
            'nbHostsIgnored'    : summaryData['hostsIgnored'],
            'nbHostsDuplicated' : summaryData['hostsDuplicated'],
            'nbServicesTotal'   : summaryData['servicesTotal'],
            'nbCommandsTotal'   : summaryData['commandsTotal'],
            'nbChecksPerHour'   : summaryData['nbChecksPerHour']
            })
