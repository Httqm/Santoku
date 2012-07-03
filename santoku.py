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


from modules import commands
from modules import config
from modules import csv
from modules import debug
from modules import fichier
from modules import hostgroups
from modules import hosts
from modules import services
from modules import summary
from modules import timer

globalTimer=timer.Timer()


############################################ ##########################################################
### main()
############################################ ##########################################################
allCommands = commands.AllCommands()
debug       = debug.Debug()

allHosts    = hosts.AllHosts()
hostgroups  = hostgroups.Hostgroups()

csv         = csv.Csv({'fileName' : config.csvFileName})
host        = hosts.Host({
                'csv'       : csv,
                'allHosts'  : allHosts
                })

allServices = services.AllServices()
serviceList = allServices.getList(csv.header)

########################################## ##########################################################
# Looping on hosts
########################################## ##########################################################
for hostId in csv.data:
    csv.setCurrentRow(hostId)

#    debug.show(csv.getCellFromCurrentRow('host_name'))
#    debug.show(str(hostId) + ' ==> ' + csv.data[hostId]['host_name'])
    
    if host.isMarkedToBeIgnored() :
        allHosts.incrementCountOf('ignored')
#	debug.show(csv.getCellFromCurrentRow('host_name') + ' IS IGNORED')
        continue

#    if(csv.currentRowHasCheckCommand()):
#	debug.show(csv.getCellFromCurrentRow('host_name') + ' HAS CHECK_COMMAND')
#        allCommands.add(host.getCheckCommand())    # TODO (later)


    if host.isDuplicated():
        allHosts.incrementCountOf('duplicated')
    else:
        csv.setHostDirectives({'hostDirectives' : host.loadDirectives() }) # TODO : hardcoded stuff ?
        allHosts.output += host.applyHostPattern()

        allHosts.incrementCountOf('valid')
        hostgroups.addHostToGroups({
            'host'      : csv.getCellFromCurrentRow('host_name'),
            'groups'    : host.loadHostGroupsFromCsv()
            })

    ###################################### ##########################################################
    # Looping on services
    ###################################### ##########################################################

    # serviceList is the list of all '*:do' CSV columns : ['check_something:do', 'check_somestuff:do', ...]
    for singleServiceCsvName in serviceList:

        service = services.Service({
            'csv'               : csv,
            'currentCsvLine'    : csv.getCurrentRow(),
            'serviceCsvName'    : singleServiceCsvName
            })

        if service.isEnabled():
            allCommands.add(service.getCommand())

            serviceName         = service.getName()
            serviceDirectives   = ''

            if service.hasDirectives():
                service.loadDirectivesFromCsvData()
                serviceDirectives = service.applyServiceDirectivesPattern()

            service.buildArrayOfServices({
                'name'              : serviceName,
                'hostName'          : csv.getCellFromCurrentRow('host_name'),
                'csvHeader'         : csv.header,
                'csvDataLine'       : csv.getCurrentRow(),
                'serviceDirectives' : serviceDirectives
                })

            allServices.output += service.make(allServices)	# <== TODO : clean this

    ###################################### ##########################################################
    # /Looping on services
    ###################################### ##########################################################

########################################## ##########################################################
# /Looping on hosts
########################################## ##########################################################

allHosts.output += hostgroups.make()


########################################## ##########################################################
# Write results to files
########################################## ##########################################################

outputFileHosts     = fichier.Fichier({ 'name' : config.outputPath+config.outputFileHosts })
outputFileHosts.write(allHosts.output)

outputFileServices  = fichier.Fichier({ 'name' : config.outputPath+config.outputFileServices })
outputFileServices.write(allServices.output)

outputFileCommands  = fichier.Fichier({ 'name' : config.outputPath+config.outputFileCommands })
outputFileCommands.write(allCommands.getOutput())


########################################## ##########################################################
# Summary
########################################## ##########################################################

summary = summary.Summary()
print summary.make({
    'hostsTotal'        : allHosts.number['valid'] + allHosts.number['ignored'],
    'hostsValid'        : allHosts.number['valid'],
    'hostsIgnored'      : allHosts.number['ignored'],
    'hostsDuplicated'   : allHosts.number['duplicated'],
    'servicesTotal'     : allServices.number,
    'commandsTotal'     : allCommands.number
    })

########################################## ##########################################################
# the end!
########################################## ##########################################################


















##from modules import commands
##from modules import fichier
##from modules import hostgroups
##from modules import pattern
##from modules import services
##from modules import summary
##
### local names for imported classes
##AllCommands = commands.AllCommands
##AllHosts    = hosts.AllHosts
##AllServices = services.AllServices
##FileIni     = fichier.FileIni
##FileOutput  = fichier.FileOutput
##Hostgroups  = hostgroups.Hostgroups
##Pattern     = pattern.Pattern
##Service     = services.Service
##Summary     = summary.Summary
##
############################################ ##########################################################
### main()
############################################ ##########################################################
##controller  = Controller()
##
##controller.checkConfigValues()
##
##csvThing    = Csv()
##allCommands = AllCommands()
##allHosts    = AllHosts()
##hostgroups  = Hostgroups()
##allServices = AllServices()
##serviceList = allServices.getList(csvThing.getHeader())
##
##
############################################ ##########################################################
### Looping on hosts
############################################ ##########################################################
##host = Host({
##    'csv'       : csvThing,
##    'allHosts'  : allHosts
##    })
##
##for hostId in csvThing.getKeys():
##
##    csvThing.setCurrentRow({'rowId' : hostId})
##
##    """
##    host = Host({
##        'csv'       : csvThing,
##        'allHosts'  : allHosts
##        })
##    """
##    if host.isMarkedToBeIgnored() :
##        allHosts.incrementCountOf('ignored')
##        continue
##
##    if(csvThing.currentRowHasCheckCommand()):
##        allCommands.add(host.getCheckCommand())
##
##    if host.isDuplicated():
##        allHosts.incrementCountOf('duplicated')
##    else:
##        csvThing.setHostDirectives({'hostDirectives' : host.loadDirectives() })
##        allHosts.output += host.applyHostPattern(csvThing.getCurrentRow())
##        allHosts.incrementCountOf('valid')
##        hostgroups.addHostToGroups({
##            'host'      : csvThing.getHostnameFromCurrentRow(),
##            'groups'    : host.loadHostGroupsFromCsv()
##            })
##
##    ################################## ##########################################################
##    # Looping on services
##    ################################## ##########################################################
##
##    # serviceList is the list of all '*:do' CSV columns : ['check_filesystem:do', 'check_bidule:do']
##    for singleServiceCsvName in serviceList:
##
##        service = Service({
##            'csv'               : csvThing,
##            'currentCsvLine'    : csvThing.getCurrentRow(),
##            'serviceCsvName'    : singleServiceCsvName
##            })
##
##        if service.isEnabled():
##            allCommands.add(service.getCommand())
##
##            serviceName         = service.getName()
##            serviceDirectives   = ''
##
##            if service.hasDirectives():
##                service.loadDirectivesFromCsvData()
##                serviceDirectives = service.applyServiceDirectivesPattern()
##
##            service.buildArrayOfServices({
##                'name'              : serviceName,
##                'hostName'          : csvThing.getHostnameFromCurrentRow(),
##                'csvHeader'         : csvThing.getHeader(),
##                'csvDataLine'       : csvThing.getCurrentRow(),
##                'serviceDirectives' : serviceDirectives
##                })
##
##            allServices.output += service.make(allServices)	# <== TODO : clean this
##
##
### host loop done : we've seen all hosts. Let's build hostgroups
##allHosts.output += hostgroups.make()
##
############################################ ##########################################################
### Write results to files
############################################ ##########################################################
##
##outputFileHosts     = FileOutput({ 'name' : config.outputPath+config.outputFileHosts })
##outputFileHosts.write(allHosts.output)
##
##outputFileServices  = FileOutput({ 'name' : config.outputPath+config.outputFileServices })
##outputFileServices.write(allServices.output)
##
##outputFileCommands  = FileOutput({ 'name' : config.outputPath+config.outputFileCommands })
##outputFileCommands.write(allCommands.getOutput())
##
##
############################################ ##########################################################
### Summary
############################################ ##########################################################
##
##summary = Summary()
##print summary.make({
##    'hostsTotal'        : allHosts.number['valid']+allHosts.number['ignored'],
##    'hostsValid'        : allHosts.number['valid'],
##    'hostsIgnored'      : allHosts.number['ignored'],
##    'hostsDuplicated'   : allHosts.number['duplicated'],
##    'servicesTotal'     : allServices.number,
##    'commandsTotal'     : allCommands.number
##    })

########################################## ##########################################################
# the end!
########################################## ##########################################################
print globalTimer.stop()
