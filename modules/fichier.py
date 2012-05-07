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
import re


controller=controller.Controller()


########################################## ##########################################################
# Generic
########################################## ##########################################################
class Fichier(object):
	def __init__(self,params):
		""" Any file. """
		self.name	= params['name']
		self.fs		= params['fs']
#		self.controller	= params['controller']
		self.data	= None


	def getData(self):
		""" Used by CSV and CFG extensions of class Fichier. """
		result=self.loadData()
		if(result):
#			self.controller.die({ 'exitMessage' : 'Error during loadData().'})
			controller=controller.Controller()
			controller.die({ 'exitMessage' : 'Error during loadData().'})
		else:
			self.check()
			return self.data
		return 0


########################################## ##########################################################
# .ini files (input)
########################################## ##########################################################
class FileIni(Fichier):
	def check(self):
		"""
		Make sure that all tags ( "$ANYTHING$" ) appearing in 'pattern' also appear in 'VARIABLE2TAG'.
		"""
		self.checkUnidirectional({
			'needle'	: config.iniPatternString,
			'haystack'	: config.iniVarToTagString
			})

		self.checkUnidirectional({
			'needle'	: config.iniVarToTagString,
			'haystack'	: config.iniPatternString
			})
		return 0


	def checkUnidirectional(self,params):
		"""
		Get ALL needles from the 'needlesStanza', and look for them in the 'haystackStanza'.
		Needles are tags surrounded with '$' signs, i.e. : $EXAMPLETAG$
		"""
		# There might be a cleaner way TODO this ;-)
		if type(self.data[params['needle']]).__name__=='str':
			needlesStanza	= self.data[params['needle']].split("\n")
		else:
			needlesStanza	= self.data[params['needle']]

		haystackStanza	= str(self.data[params['haystack']])


		"""
		print 'NEEDLE'
		print needlesStanza
		print 'HAYSTACK'
		print haystackStanza 
		print '-----------------------------------------'
		"""
		for line in needlesStanza:
			match	= re.search('\$([^\$]+)\$', line)
			if(match):

				match2	= re.search('('+match.group(1)+')',haystackStanza)
#				print 'MATCH1 : '+match.group(1)
#				print 'MATCH2 : '+match2.group(1)
				
				if(not match2):
#					self.controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+params['needle']+'" block, missing in "'+params['haystack']+'" block.'})
#					controller=controller.Controller()
					controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+params['needle']+'" block, missing in "'+params['haystack']+'" block.'})

		return 0


	def loadData(self):
		""" Read data from config file. """
		try:
			cfgFile = open(self.name, 'r')
		except IOError, e:	# trap IOError only
#			self.controller.die({ 'exitMessage' : 'Expected file "'+self.name+'" not found.'})
			controller=controller.Controller()
			controller.die({ 'exitMessage' : 'Expected file "'+self.name+'" not found.'})

		srcData		= {}
		sectionType	= ''
		for line in cfgFile:
			# skip comments line in cfg file
			match=re.search('^#', line)
			if(match):
				continue

			# searching a '[...]' section
			match=re.search('\[(.+)\]', line)
			if(match):
				# found a section. Let's detect which kind of section it is
				sectionType=match.group(1)	# could be 'pattern' or 'VARIABLE2TAG', or ...
				if(sectionType==config.iniPatternString):
					srcData[sectionType]=''		# create key in data hash
				elif(sectionType==config.iniVarToTagString):
					srcData[sectionType]={}		# create key in data hash

			else:
				# loading data from section
				if(sectionType==config.iniPatternString):
					srcData[sectionType]+=line

				elif(sectionType==config.iniVarToTagString):
					# trim file content
					line=line.replace(' ', '')
					line=line.replace("\t", '')	# UGLY !!!
					# TODO : make sure config.iniVarToTagStanzaFs is found here
					match=re.search('^(.+)'+config.iniVarToTagStanzaFs+'(.+)$', line)
					if(match):
						# csvField => tag
						#srcData[sectionType][match.group(1)]=match.group(2)
						# tag ==> csvField
						srcData[sectionType][match.group(2)]=match.group(1)

		self.data	= srcData
		return 		0	# Unix-style : 0 is OK




########################################## ##########################################################
# an input CSV file
########################################## ##########################################################
class FileCsv(Fichier):

	def check(self):
		"""
		Does nothing so far.
		Just to match the Fichier.getData() method requirement.
		"""
		return 0


	def loadData(self):
		""" Load data from CSV file into a dictionary """
		self.getColumnNumbers()
		self.readCsvDataIgnoringHeaders()
		return 		0	# Unix-style : 0 is OK


	def readCsvDataIgnoringHeaders(self):
		"""
		Read the data contained in the CSV file, ignoring the header line
		"""
		import fileinput
		csvData	= {}
		lineNb	= 0
		for line in fileinput.input([self.name]):

			# skip CSV headers line
			lineNb+=1
			if(lineNb==1):
				continue

			ligne		= line.split(self.fs)
			host_name	= ligne[self.columnTextToNumber[config.csvHeaderHostName]].strip('"')
			hostFields	= {}

			for clefs in self.columNumberToText.keys():
				hostFields[self.columNumberToText[clefs]]=ligne[clefs].strip('"')

			csvData[host_name]=hostFields

		self.data	= csvData

		return 		0	# Unix-style : 0 is OK


	def getColumnNumbers(self):
		"""
		Read the first line of the CSV file, hthen builds 2 dictionaries :
		- column number to column text
		- column text to column number
		"""
		try:
			infile		= open(self.name,'r')
			self.header	= infile.readline()
		except IOError:
#			self.controller.die({ 'exitMessage' : 'Source CSV file "'+self.name+'" declared in "'+config.configFile+'" not found.'})
			controller=controller.Controller()
			controller.die({ 'exitMessage' : 'Source CSV file "'+self.name+'" declared in "'+config.configFile+'" not found.'})

		self.columNumberToText	= {}
		self.columnTextToNumber = {}
		champs			= self.header.split(self.fs)
		columnNumber		= 0

		for champ in champs:
			tmp				= champ.strip('"')
			self.columNumberToText[columnNumber]	= tmp
			self.columnTextToNumber[tmp]		= columnNumber
			columnNumber+=1

		return 0


	def getHeader(self):
		""" Return the header of the CSV file as a list of fields. """
		return self.header.replace('"', '').split(self.fs)


	def columnExists(self,columnHeader):
		""" Return 'true' if the specified column name exists (found in CSV headers). """
		return 1 if columnHeader in self.getHeader() else 0



########################################## ##########################################################
# Output files 
########################################## ##########################################################
class FileOutput(Fichier):
	def __init__(self,params):
		""" Extends class 'fichier' """
		self.name	= params['name']


	def makeHeader(self):
		""" Generate a basic header for output files showing generation date + 'do not modify manually' warning """

		import datetime
		now		= datetime.datetime.now()
		self.header	= "########################################## ##########################################################\n\
# "+self.name+"\n# Generated by Santoku on "+now.strftime("%Y/%m/%d %H:%M")+"\n\
# Don't edit manually or changes might be overwritten !\n\
########################################## ##########################################################\n\n"
		return 0	# Unix-style : 0 is OK

		
	def getHeader(self):
		""" Return the output file header """
		if(self.makeHeader()):
			raise Exception, 'Can not get header for output file' # TODO : clean this!
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
#			self.controller.die({ 'exitMessage' : 'Can not write results to "'+self.name+'" : '+str(e)})
			controller=controller.Controller()
			controller.die({ 'exitMessage' : 'Can not write results to "'+self.name+'" : '+str(e)})
