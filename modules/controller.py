#!/usr/bin/python

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

