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

class Pattern(object):

    def __init__(self, params):
        """
        A pattern is used to substitute tags with values and build .cfg files.

        - pattern is a block of text containing tags identified by special chars. ex : $TAG$. Patterns and tags are defined in .ini files.
        - values : dictionary with key = variable name, and value = ... value ;-)
        """
        self._file      = params['file']    # used in debug messages only
        self._pattern   = params['pattern']
        self.searchTags()


    def searchTags(self):
        import re
        tagRegExp   = '\\' + config.iniTagChar + '(.*)\\b'
        tagList     = re.findall(tagRegExp, self._pattern)
        if(not tagList):
            debug.die({'exitMessage': 'No tag matching pattern "' + tagRegExp + '" found in "' + self._file + '"'})
        return tagList


    def apply(self, values):
        """ Perform substitutions of tags with their values in the pattern """
        from string import Template
        template = Template(self._pattern)
        try:
            patternWithSubstitutedValues = template.safe_substitute(values)
            return patternWithSubstitutedValues
        # TODO : exceptions below are not optimal :-(
        except NameError as e:
            debug.die({'exitMessage': '(pattern.py) key error : ' + str(e) })
        except KeyError as e:
            debug.show('key error : ' + e.strerror)
            return None
