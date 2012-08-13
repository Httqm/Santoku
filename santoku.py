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
#from modules import timer


########################################## ##########################################################
# main()
########################################## ##########################################################
allCommands = commands.AllCommands()
debug       = debug.Debug()

allHosts    = hosts.AllHosts()

hostgroups  = hostgroups.Hostgroups()

csv         = csv.Csv({'fileName': config.csvFileName})
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

    if host.isMarkedToBeIgnored():
        allHosts.incrementCountOf('ignored')
        continue

    # TODO / BUG ? : if a host is duplicated, only the values on its 1st host definition will be considered
    if host.isAlreadyRegisteredInHostsCfg():
        allHosts.incrementCountOf('duplicated')
    else:
        allHosts.incrementCountOf('valid')
        csv.setHostDirectives({'hostDirectives': host.loadDirectives() })
        allHosts.output += host.applyHostPattern()
        hostgroups.addHostToGroups({
            'host'      : csv.getCellFromCurrentRow(config.csvHeaderHostName),
            'groups'    : host.loadHostGroupsFromCsv()
            })

    if(csv.currentRowHasCheckCommand()):
        allCommands.add(host.getCheckCommand())
        allServices.countChecksPerHour(host.getCheckInterval())

    ###################################### ##########################################################
    # Looping on services
    ###################################### ##########################################################

    # serviceList is the list of all '*:do' CSV columns : ['check_something:do', 'check_somestuff:do', ...]
    for singleServiceCsvName in serviceList:

        service = services.Service({
            'csv'               : csv,
            'currentCsvLine'    : csv.getCurrentRow(),
            'serviceCsvName'    : singleServiceCsvName,
            'allServices'       : allServices
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
                'csvDataLine'       : csv.getCurrentRow(),
                'serviceDirectives' : serviceDirectives
                })

            allServices.output += service.make()


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

allHosts.clean()
outputFileHosts     = fichier.Fichier({'name': config.outputPath+config.outputFileHosts})
outputFileHosts.write(allHosts.output)

outputFileServices  = fichier.Fichier({'name': config.outputPath+config.outputFileServices})
outputFileServices.write(allServices.output)

outputFileCommands  = fichier.Fichier({'name': config.outputPath+config.outputFileCommands})
outputFileCommands.write(allCommands.getOutput())

########################################## ##########################################################
# Summary
########################################## ##########################################################

summary = summary.Summary()
print (summary.make({
    'nbLines'           : csv.nbLines,
    'hostsTotal'        : allHosts.number['valid'] + allHosts.number['ignored'],
    'hostsValid'        : allHosts.number['valid'],
    'hostsIgnored'      : allHosts.number['ignored'],
    'hostsDuplicated'   : allHosts.number['duplicated'],
    'servicesTotal'     : allServices.number,
    'commandsTotal'     : allCommands.number,
    'nbChecksPerHour'   : allServices.nbChecksPerHour
    }))

########################################## ##########################################################
# the end!
########################################## ##########################################################
