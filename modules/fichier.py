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



from modules import config as c
import re

########################################## ##########################################################
# Generic
########################################## ##########################################################
class Fichier(object):	# 'object' : ancestor of all classes
	def __init__(self,params):
		""" Any file. """
		self.name	= params['name']
		self.fs		= params['fs']
		self.controller	= params['controller']
		self.data	= None

	"""
	def getData(self):
		#Used by CSV and CFG extensions of class Fichier.
		result=self.loadData()
		if(result):
			# TODO : leave with controller
			print str(result)
			import sys
			sys.exit(1)	# http://docs.python.org/library/sys.html?highlight=sys.exit#sys.exit
		else:
			return self.data
		return 0
	"""

	def getData(self):
		""" Used by CSV and CFG extensions of class Fichier. """
		result=self.loadData()
		if(result):
			self.controller.die({ 'exitMessage' : 'Error during loadData().'})
		else:
			self.check()
			return self.data
		return 0


########################################## ##########################################################
# .ini files (input)
########################################## ##########################################################
class FileInIni(Fichier):

	"""
	def __init__(self,params):
		#Extends class 'fichier'. Specializes on CFG files. 
		self.name	= params['name']
		self.data	= None
		self.controller	= params['controller']
	"""

	def check(self):
		"""
		Make sure that all tags ( "$ANYTHING$" ) appearing in 'pattern' also appear in 'VARIABLE2TAG'.
		"""
		self.checkUnidirectional({
			'needle'	: c.iniPatternString,
			'haystack'	: c.iniVarToTagString
			})

		self.checkUnidirectional({
			'needle'	: c.iniVarToTagString,
			'haystack'	: c.iniPatternString
			})


		"""
		# STEP 1 : make sure that ALL '$$' found in 'pattern' block exist in 'VARIABLE2TAG' block
		# loading '$something$' from the 'pattern' block
		patternLines	= self.data[c.iniPatternString].split("\n")
		varToTagBlock	= str(self.data[c.iniVarToTagString])
		for patternLine in patternLines:

			# searching '$something$' in the 'pattern' block
			match	= re.search('\$([^\$]+)\$', patternLine)
			if(match):
				# searching similar '$something$' in the 'varToTag' block
				match2	= re.search('('+match.group(1)+')',varToTagBlock)
				if(not match2):
					self.controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+c.iniPatternString+'" block, missing in "'+c.iniVarToTagString+'" block.'})

		"""

		"""
		# STEP 2 : make sure that ALL '$$' found in 'VARIABLE2TAG' block exist in 'pattern' block
		# loading '$something$' from the 'VARIABLE2TAG' block : the '$$' are the keys
		varToTagLines=self.data[c.iniVarToTagString]
		patternBlock= str(self.data[c.iniPatternString])
		for varToTagLine in varToTagLines:
			# searching '$something$' in the 'varToTag' block
			match	= re.search('\$([^\$]+)\$', varToTagLine)
			if(match):
				# searching similar '$something$' in the 'pattern' block
				match2	= re.search('('+match.group(1)+')',patternBlock)
				if(not match2):
					self.controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+c.iniVarToTagString+'" block, missing in "'+c.iniPatternString+'" block.'})
		"""
		return 0


	def checkUnidirectional(self,params):
		"""
		Get ALL needles from the 'needlesStanza', and look for them in the 'haystackStanza'.
		Needles are tags surrounded with '$' signs, i.e. : $EXAMPLETAG$
		"""

		# There might be a cleaner way TODO this ;-)
		# c.iniVarToTagStanzaFs
		#print params['needle']+' : '+str(type(self.data[params['needle']]))
		if type(self.data[params['needle']]).__name__=='str':
			needlesStanza	= self.data[params['needle']].split("\n")
		else:
			needlesStanza	= self.data[params['needle']]

		haystackStanza	= str(self.data[params['haystack']])

		#print haystackStanza

		for line in needlesStanza:
			match	= re.search('\$([^\$]+)\$', line)
			if(match):
				match2	= re.search('('+match.group(1)+')',haystackStanza)
				if(not match2):
					self.controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+params['needle']+'" block, missing in "'+params['haystack']+'" block.'})


		return 0



	def loadData(self):
		""" Read data from config file. """
		# http://docs.python.org/tutorial/inputoutput.html
		try:
			cfgFile = open(self.name, 'r')
		except IOError, e:	# trap IOError only
			self.controller.die({ 'exitMessage' : 'Expected file "'+self.name+'" not found.'})

		"""		
		except Exception, e :	# trap all exceptions
#			print str(e)	# IOError: [Errno 2] No such file or directory: './config/hosts.ini'
#			print e.args[1]


			# no specific error message so far. TODO
			self.controller.die({ 'exitMessage' : str(e)})
		# finally : http://docs.python.org/reference/compound_stmts.html#finally

		except:
			# basic error handling
			# TODO : write to log string on error
			return 1
		"""
		srcData={}

		sectionType	= ''
		for line in cfgFile:
			# skip comments line in cfg file
			match=re.search('^#', line)
			if(match):
				continue
			# switch-case in Python : http://bytebaker.com/2008/11/03/switch-case-statement-in-python/

			# searching a '[...]' section
			match=re.search('\[(.+)\]', line)
			if(match):
				# found a section. Let's detect which kind of section it is
				sectionType=match.group(1)	# could be 'pattern' or 'VARIABLE2TAG', or ...
				if(sectionType==c.iniPatternString):
					srcData[sectionType]=''		# create key in data hash
				elif(sectionType==c.iniVarToTagString):
					srcData[sectionType]={}		# create key in data hash

			else:
				# loading data from section
				if(sectionType==c.iniPatternString):
					srcData[sectionType]+=line

				elif(sectionType==c.iniVarToTagString):
					# trim file content
					line=line.replace(' ', '')
					line=line.replace("\t", '')	# UGLY !!!
#					line=''.strip(line)	# http://docs.python.org/library/string.html#string.strip DEPRECATED ?
#					print line
					#match=re.search('^(.+):(.+)$', line)
					#print '============== RE = ^(.+)'+c.iniVarToTagStanzaFs+'(.+)$'
					# TODO : make sure c.iniVarToTagStanzaFs is found here
					match=re.search('^(.+)'+c.iniVarToTagStanzaFs+'(.+)$', line)
					if(match):
						# csvField => tag
						#srcData[sectionType][match.group(1)]=match.group(2)
						# tag ==> csvField
						srcData[sectionType][match.group(2)]=match.group(1)
		#print srcData

		self.data	= srcData
		return 		0	# Unix-style : 0 is OK




########################################## ##########################################################
# 
########################################## ##########################################################
# 1 CSV file contains hosts + services data
class FileInCsv(Fichier):

	"""
	def __init__(self,params):
		# Extends class 'fichier'. Specializes on CSV files.
		self.name	= params['name']
		self.fs		= params['fs']
	"""

	def check(self):
		"""
		Does nothing so far.
		Just to match the Fichier.getData method requirement.
		"""
		return 0

	# http://www.yak.net/fqa/171.html
	# read file line by line without loading it in memory first. the fileinput.input() call reads lines sequentially,
	# but doesn't keep them in memory after they've been read.
	def loadData(self):
		""" Load data from CSV file into a dictionary """
		import fileinput

		srcData={}

		# read 1st line to get column numbers
		try:
			infile		= open(self.name,'r')
			self.header	= infile.readline()
		except IOError:
			self.controller.die({ 'exitMessage' : 'Source CSV file "'+self.name+'" declared in "'+c.configFile+'" not found.'})


		champs		= self.header.split(self.fs)
		colNb2Text	= {}
		colNumber	= 0

                

		for champ in champs:
			colNb2Text[colNumber]=champ.strip('"')
			colNumber+=1

		# get field id of 'host_name'. 'host_name' is used as the key of our final dict.
		colText2Nb = {}
		for key, val in colNb2Text.items():
			colText2Nb[val] = key

		# read CSV file data
		lineNb=0
		for line in fileinput.input([self.name]):

			# skip CSV headers line
			lineNb+=1
			if(lineNb==1):
				continue

			ligne		= line.split(self.fs)
			host_name	= ligne[colText2Nb[c.csvHeaderHostName]].strip('"')
			hostFields	= {}

			for clefs in colNb2Text.keys():
				hostFields[colNb2Text[clefs]]=ligne[clefs].strip('"')

			srcData[host_name]=hostFields

			"""
			# if (any error):
			#	raise Exception, 'Can not load data from CSV file "'+srcFile+'"'	# or params['name'] ? Or deal with this in the class ?
			http://python.about.com/od/gettingstarted/ss/begpyexceptions_8.htm
			http://python.about.com/od/pythonstandardlibrary/a/lib_exceptions.htm
			"""

		self.data	= srcData
		return 		0	# Unix-style : 0 is OK


	def getHeader(self):
		""" Return the header of the CSV file as a list of fields. """
		return self.header.replace('"', '').split(self.fs)


	def columnExists(self,columnHeader):
		""" Return 'true' if the specified column name exists (found in CSV headers). """
		return 1 if columnHeader in self.getHeader() else 0



########################################## ##########################################################
# 
########################################## ##########################################################
class FileOut(Fichier):
	def __init__(self,params):
		""" Extends class 'fichier' """
		self.name	= params['name']


	def makeHeader(self):
		""" Generate a basic header for output files showing generation date + 'do not modify manually' warning """

		# http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
		import datetime
		now = datetime.datetime.now()
		self.header="########################################## ##########################################################\n\
# "+self.name+"\n# Generated by Santoku on "+now.strftime("%Y/%m/%d %H:%M")+"\n\
# Don't edit manually or changes might be overwritten !\n\
########################################## ##########################################################\n\n"
		return 0	# Unix-style : 0 is OK

		
	def getHeader(self):
		""" Return the output file header """
		if(self.makeHeader()):
			raise Exception, 'Can not get header for output file'
		else:
			return self.header

	def write(self, data):
		""" Write data to file """
		try:
			outFile	= open(self.name,'w')
			outFile.write(self.getHeader())
			outFile.write(data)
			outFile.close
		except Exception, e :
			print str(e)
			import sys
			sys.exit(1)	# http://docs.python.org/library/sys.html?highlight=sys.exit#sys.exit

