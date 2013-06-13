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


class Debug(object):

    def __init__(self):
        self._mySys = __import__('sys')


    def die(self, exitMessage, exitCode=2):
        """
        Display an error message and leave the program.

        The defaut exit code is 2 to identify cases when a script was terminated through this function.
        """
        print (exitMessage)
        print (config.messageDie)
        self._mySys.exit(exitCode)


    def show(self, message):
        if config.debug:
            import inspect
            print ("\n" \
                + " ++=================== DEBUG =========================\n" \
                + ' || FILE    : ' + str(inspect.stack()[1][1]) + "\n" \
                + ' || LINE    : ' + str(inspect.stack()[1][2]) + "\n" \
                + ' || CALLER  : ' + str(inspect.stack()[1][3]) + "\n" \
                + ' || MESSAGE : ' + str(message) + "\n" \
                + " ++================== /DEBUG =========================\n")

    #TODO :
    # 1. add an 'enable' method to toggle display of debug messages
