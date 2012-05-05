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


########################################## ##########################################################
# 
########################################## ##########################################################

# die : http://www.velocityreviews.com/forums/t359278-how-to-stop-python.html

class Controller(object):	# 'object' : ancestor of all classes
	def __init__(self):
            """ """
            self.mySys	= __import__('sys')	# http://effbot.org/zone/import-confusion.htm
            from modules import config as c
            self.c=c	# looking for a cleaner way to do this ;-)


	def die(self,params):
            """ Display an error message and leave the program. """
            print params['exitMessage']
            print self.c.messageDie
            self.mySys.exit(2)	# http://docs.python.org/library/sys.html#sys.exit

