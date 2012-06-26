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
from modules import controller
controller = controller.Controller()


class Pattern(object):

    def __init__(self,params):
        """
        A pattern is used to substitute tags with values and build .cfg files.

        - pattern is a block of text containing tags identified by special chars. ex : $TAG$. Patterns and tags are defined in .ini files.
        - variable2tag : dictionary with key = variable name, and value = tag name. This is defined in the [VARIABLE2TAG] section of .ini files
        - values : dictionary with key = variable name, and value = ... value ;-)
        """
        self.file           = params['file']
        self.pattern        = params['pattern']
        self.variable2tag   = params['variable2tag']


    def apply(self,values):
        """ Perform substitutions of tags with their values in the pattern """
        patternCopy = self.pattern  # so that pattern is not altered
        self.values = values
        for tag in self.variable2tag:
            self.checkTagValueExists(tag)
            patternCopy	= patternCopy.replace(tag,str(self.values[self.variable2tag[tag]]))
            # /!\ args for replace must be strings. Otherwise "expected a character buffer object" error
        return patternCopy


    def checkTagValueExists(self,tag):
        try:
            self.values[self.variable2tag[tag]]
        except KeyError:
            controller.die({ 'exitMessage' : 'No CSV value given for tag "' + tag + "\" in pattern :\n\n" + self.pattern + "\nMake sure the column names listed in the \"[" + config.iniVarToTagString + ']" stanza of "' + self.file + '" REALLY match "' + config.configFilesPath + config.csvFileName + '" column names.' })
#            controller.die({ 'exitMessage' : 'No CSV value given for tag "' + tag + '" in pattern : ' + self.pattern })
