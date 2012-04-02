#!/usr/bin/python

"""
http://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
"""

########################################## ##########################################################
# 
########################################## ##########################################################
class Pattern(object):	# 'object' : ancestor of all classes
	def __init__(self,params):
		"""
		A pattern is used to substitute tags with values and build .cfg files.

		- pattern is a block of text containing tags identified by special chars. ex : $TAG$. Patterns and tags are defined in .ini files.
		- variable2tag : dictionary with key = variable name, and value = tag name. This is defined in the [VARIABLE2TAG] section of .ini files
		- values : dictionary with key = variable name, and value = ... value ;-)
		"""
		self.pattern		= params['pattern']
		self.variable2tag	= params['variable2tag']


	def apply(self,values):
		""" Perform substitutions over a copy of the pattern, so that the pattern is not altered """
		patternCopy		= self.pattern	# so that pattern is not altered
		values			= values

		for tag in self.variable2tag:
			patternCopy=patternCopy.replace(tag,values[self.variable2tag[tag]])

		return patternCopy

