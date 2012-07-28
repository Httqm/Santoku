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


class Directives(object):

    def compareNumberOfNamesAndValues(self, params):
        sameNumberOfNamesAndValues = (len(params['names'])) == (len(params['values']))
        if (not sameNumberOfNamesAndValues):
            debug.die({'exitMessage': 'Error in source file "' + config.csvFileName + '" for host "' + params['hostName'] \
                + '" (line ' + str(params['csvLineNumber']) + ') : columns "' \
                + config.csvHostDirectivesNames + '" and "' + config.csvHostDirectivesValues \
                + '" don\'t have the same number of parameters.'
                })


