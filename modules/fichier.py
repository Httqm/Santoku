########################################## ##########################################################
# 
########################################## ##########################################################
class Fichier(object):	# 'object' : ancestor of all classes
	def __init__(self,name):
		""" Any file """
		self.name='noName'

	def getData(self):
		""" Used by CSV and CFG extensions of Fichier. """
		result=self.loadData()
		if(result):
			print str(result)
			import sys
			sys.exit(1)	# http://docs.python.org/library/sys.html?highlight=sys.exit#sys.exit
		else:
			return self.data


########################################## ##########################################################
# 
########################################## ##########################################################
# n CFG files contain config data : patterns, tags, ...
class FileInIni(Fichier):
	def __init__(self,params):
		""" Extends class 'fichier'. Specializes on CFG files. """
		#self.dir	= params['dir']
		self.name	= params['name']
		self.data	= None

	def loadData(self):
		""" Read data from config file """
		# http://docs.python.org/tutorial/inputoutput.html
		try:
			cfgFile = open(self.name, 'r')
#		except IOError, e:	# trap IOError only
		except Exception, e :	# trap all exceptions
#			print str(e)	# IOError: [Errno 2] No such file or directory: './config/hosts.ini'
#			print e.args[1]
#			return 1
			return e
		# finally : http://docs.python.org/reference/compound_stmts.html#finally
		"""
		except:
			# basic error handling
			# TODO : write to log string on error
			return 1
		"""
		srcData={}
		import re	# for RegExp

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
#				print 'found section :'+match.group(1)
				sectionType=match.group(1)	# could be 'pattern' or 'VARIABLE2TAG', or ...
				if(sectionType=='pattern'):
					srcData[sectionType]=''		# create key in data hash
				elif(sectionType=='VARIABLE2TAG'):
					srcData[sectionType]={}		# create key in data hash

			else:
				# loading data from section
				if(sectionType=='pattern'):
					srcData[sectionType]+=line

				elif(sectionType=='VARIABLE2TAG'):
					# trim file content
					line=line.replace(' ', '')
					line=line.replace("\t", '')	# UGLY !!!
#					line=''.strip(line)	# http://docs.python.org/library/string.html#string.strip DEPRECATED ?
#					print line
					match=re.search('^(.+):(.+)$', line)
					if(match):
						# csvField => tag
						#srcData[sectionType][match.group(1)]=match.group(2)
						# tag ==> csvField
						srcData[sectionType][match.group(2)]=match.group(1)
		self.data	= srcData
		return 		0	# Unix-style : 0 is OK




########################################## ##########################################################
# 
########################################## ##########################################################
# 1 CSV file contains hosts + services data
class FileInCsv(Fichier):
	def __init__(self,params):
		""" Extends class 'fichier'. Specializes on CSV files. """
		self.name	= params['name']
		self.fs		= params['fs']


	# http://www.yak.net/fqa/171.html
	# read file line by line without loading it in memory first. the fileinput.input() call reads lines sequentially,
	# but doesn't keep them in memory after they've been read.
	def loadData(self):
		""" Load data from CSV file into a dictionary """
		import fileinput

		srcData={}

		# read 1st line to get column numbers
		infile		= open(self.name,'r')
		self.header	= infile.readline()
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
			host_name	= ligne[colText2Nb['host_name']].strip('"')
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

