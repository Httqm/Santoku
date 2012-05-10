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
		self.data	= None


	def getData(self):
		self.loadData()
		self.checkLoadedData()
		return self.data


########################################## ##########################################################
# .ini files (input)
########################################## ##########################################################
class FileIni(Fichier):

	def checkLoadedData(self):
		"""
		Make sure that all tags ( "$ANYTHING$" ) appearing in 'pattern' also appear in 'VARIABLE2TAG'.
		And vice-versa.
		"""
		self.checkStanzasTitlesAreFoundInIniFileLoadedData()
		self.checkTagsBetweenStanzas({
			'needle'	: config.iniPatternString,
			'haystack'	: config.iniVarToTagString
			})

		self.checkTagsBetweenStanzas({
			'needle'	: config.iniVarToTagString,
			'haystack'	: config.iniPatternString
			})


	def checkStanzasTitlesAreFoundInIniFileLoadedData(self):
		self.searchStanzaTitleInIniFileLoadedData(config.iniPatternString)
		self.searchStanzaTitleInIniFileLoadedData(config.iniVarToTagString)


	def searchStanzaTitleInIniFileLoadedData(self,key):
		try:
			self.data[key]
		except Exception:
			controller.die({ 'exitMessage' : '"'+key+'" keyword not found in "'+self.name+'"'})


	def checkTagsBetweenStanzas(self,params):
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
		for line in needlesStanza:
			match	= re.search('\$([^\$]+)\$', line)
			if(match):
				match2	= re.search('(\$'+match.group(1)+'\$)',haystackStanza)
				if(not match2):
					controller.die({ 'exitMessage' : self.name+' : Tag "'+match.group(1)+'" found in "'+params['needle']+'" block, missing in "'+params['haystack']+'" block.'})


	def loadData(self):
		self.checkFileIsThere()
		self.data		= {}
		self.sectionType	= ''
		for line in self.iniFile:

			if self.lineIsNotAComment(line) and self.lineIsNotBlank(line):
				# searching a '[...]' section
				match	= re.search('\[(.+)\]', line)
				if(match):
					# found a section. Let's detect which kind of section it is
					self.sectionType	= match.group(1)		# could be 'pattern' or 'VARIABLE2TAG', or ...
					if(self.sectionType	== config.iniPatternString):
						self.data[self.sectionType]	= ''
					elif(self.sectionType== config.iniVarToTagString):
						self.data[self.sectionType]	= {}

				else:
					# loading data from section
					if(self.sectionType	== config.iniPatternString):
						self.data[self.sectionType]+=line

					elif(self.sectionType	== config.iniVarToTagString):
						line	= self.removeWhitespaces(line)
						self.checkLineMatchesFormat(line)
						match	= re.search('^(.+)'+config.iniVarToTagStanzaFs+'(.+)$', line)
						if(match):
							self.data[self.sectionType][match.group(2)]=match.group(1)


	def checkFileIsThere(self):
		try:
			self.iniFile = open(self.name, 'r')
		except IOError:
			controller.die({ 'exitMessage' : 'Expected file "'+self.name+'" not found.'})


	def lineIsNotAComment(self,line):
		match=re.search('^#', line)
		if(match):
			return 0
		else:
			return 1


	def lineIsNotBlank(self,line):
		match=re.search('^\n$', line)
		if(match):
			return 0
		else:
			return 1


	def removeWhitespaces(self,line):
		return line.replace(' ', '').replace("\t", '')	# works but UGLY !!!


	def checkLineMatchesFormat(self,line):
		#print 'LINE:'+line+'.'
		match=re.search('^\w+'+config.iniVarToTagStanzaFs+'\$\w+\$$', line)
		if match:
			return line
		else:
			controller.die({ 'exitMessage' : 'In file "'+self.name+'", section ['+self.sectionType+'], the line "'+line.replace("\n",'')+'" doesn\'t match the "variable '+config.iniVarToTagStanzaFs+' $TAG$" format. (not counting whitespaces).'})



########################################## ##########################################################
# an input CSV file
########################################## ##########################################################
class FileCsv(Fichier):

	def checkLoadedData(self):
		"""
		Does nothing so far.
		Just to match the Fichier.getData() method requirement.
		"""


	def loadData(self):
		""" Load data from CSV file into a dictionary """
		self.getColumnNumbers()
		self.readCsvDataIgnoringHeaders()


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
			controller.die({ 'exitMessage' : 'Source CSV file "'+self.name+'" declared in "'+config.configFile+'" not found.'})

		self.columNumberToText	= {}
		self.columnTextToNumber = {}
		champs			= self.header.split(self.fs)
		columnNumber		= 0

		for champ in champs:
			tmp					= champ.strip('"')
			self.columNumberToText[columnNumber]	= tmp
			self.columnTextToNumber[tmp]		= columnNumber
			columnNumber+=1


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
		""" Generate a basic header for output files showing generation date + a 'do not modify manually' warning """

		import datetime
		now		= datetime.datetime.now()
		return "########################################## ##########################################################\n\
# "+self.name+"\n# Generated by Santoku on "+now.strftime("%Y/%m/%d %H:%M")+"\n\
# Don't edit manually or changes might be overwritten !\n\
########################################## ##########################################################\n\n"


	def write(self, data):
		""" Write data to file """
		try:
			outFile	= open(self.name,'w')
			outFile.write(self.makeHeader())
			outFile.write(data)
			outFile.close
		except Exception, e :
			controller.die({ 'exitMessage' : 'Can not write results to "'+self.name+'" : '+str(e)})
