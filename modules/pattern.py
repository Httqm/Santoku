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

debug = debug.Debug()

# See http://docs.python.org/library/string.html#template-strings
class Pattern(object):

    def __init__(self,params):
        """
        A pattern is used to substitute tags with values and build .cfg files.

        - pattern is a block of text containing tags identified by special chars. ex : $TAG$. Patterns and tags are defined in .ini files.
        - variable2tag : dictionary with key = variable name, and value = tag name. This is defined in the [VARIABLE2TAG] section of .ini files
        - values : dictionary with key = variable name, and value = ... value ;-)
        """
        self.file           = params['file']    # used in debug messages only
        self.pattern        = params['pattern']
#        self.variable2tag   = params['variable2tag']
        self.searchTags()


    def searchTags(self):
        import re
#        tagRegExp   = '\\' + config.iniTagChar + '.*\\' + config.iniTagChar
        tagRegExp   = '\\' + config.iniTagChar + '.*\\b'
        self.tagList       = re.findall(tagRegExp, self.pattern)
        if(self.tagList):
            debug.show('FOUND : ' + str(self.tagList))
        else:    
            debug.die({'exitMessage': 'No tag matching pattern "' + tagRegExp + '" found in "' + self.file + '"'})


    def apply(self,values):
        """ Perform substitutions of tags with their values in the pattern """
#        patternCopy = self.pattern  # so that pattern is not altered # TODO : is this still necessary ?
#        debug.show('patternCopy : ' + patternCopy)
        from string import Template
#        template = Template(patternCopy)
        template = Template(self.pattern)
        try:
            patternWithSubstitutedValues = template.safe_substitute(values)
            debug.show(patternWithSubstitutedValues)
            return patternWithSubstitutedValues
        except KeyError,e: # TODO : improve this
            debug.show('key error : ' + str(e))
            return ''


    def checkTagValueExists(self,tag):
        try:
            self.values[self.variable2tag[tag]]
        except KeyError:
            debug.die({ 'exitMessage' : 'No CSV value given for tag "' + tag + "\" in pattern :\n\n" + self.pattern + "\nMake sure the column names listed in the \"[" + config.iniVarToTagString + ']" stanza of "' + self.file + '" REALLY match "' + config.configFilesPath + config.csvFileName + '" column names.' })
