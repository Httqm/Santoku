#!/usr/bin/python

########################################## ##########################################################
# 
########################################## ##########################################################
class Service(object):	# 'object' : ancestor of all classes
	def __init__(self,params):
		""" """
		self.params	= params
		self.cleanName	= self.params['name'].replace(':do','')	# <== HARDCODED. bad! The name without the ':do'

	def getName(self):
		return self.cleanName

	def loadServiceData(self):
		"""
		For the current host and the current service, return : 
		- 'clean' CSV header lines (without the 'serviceName:')
		- cell values (including multiple values and field separators if any)
		"""
		import re
		serviceCsvData={} # temporary dict

		# storing CSV data in a dict to play with it later
		for field in self.params['csvHeader']:
			match=re.search(self.cleanName+':.*', field)
			if(match):
				# parsing all CSV columns related to this service
				serviceCsvData[field.replace(self.cleanName+':','')]=self.params['csvDataLine'][field]

		# appending 'serviceDirectives'
		# serviceCsvData contains 2 useless keys : 'serviceDirectivesNames' and 'serviceDirectivesValues'
		serviceCsvData['serviceDirectives']=self.params['serviceDirectives']

		return serviceCsvData


	def buildArrayOfServices(self):
		"""
		Return an associative array containing all service(s) data ready to be injected into pattern.
		This method handle multi-valued CSV cells
		"""
		serviceCsvData	= self.loadServiceData()
		champsValeurs	= {}

		# Parsing data stored in dict to register as many services as the number of values in mutli-valued cells
		maxRounds	= 1
		currentRound	= 0

		while currentRound < maxRounds:
			champsValeurs[currentRound]	= {
				'host_name'	: self.params['host'],
				'use'		: 'generic_service'
				}
			for serviceField in serviceCsvData:
				valuesOfMultiValuedCell	= serviceCsvData[serviceField].split(self.params['fieldSeparator'])
				maxRounds		= len(valuesOfMultiValuedCell) if (len(valuesOfMultiValuedCell)>maxRounds) else maxRounds
				try:
					tmpValue	= valuesOfMultiValuedCell[currentRound]
				except IndexError:
					tmpValue	= valuesOfMultiValuedCell[0]

				champsValeurs[currentRound][serviceField]=tmpValue

			currentRound+=1
		result={
			'champsValeurs'	: champsValeurs,
			'maxRounds'	: maxRounds
			}
		return result

