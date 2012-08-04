===================================
Presentation of the Santoku project
===================================

Santoku is a utility designed to generate configuration files for Shinken and Nagios from data provided in a CSV file. The CSV file is expected to have a specific format (described in the documentation).
The generated files are :
- hosts.cfg, including host groups
- services.cfg
- commands.cfg
- and a very basic tabular-presented Nagvis map showing ALL hosts listed in the CSV file (0% done)

At a previous position, I wrote a PERL script doing all this (except the commands.cfg part). This script still works very well, but because of the numerous plugins / environments / usages it handles, it's now a 60KBytes cluttered script and debugging/updating it has become a nightmare. So I can't even share it with the community.
This is why I started developping Santoku : I wanted like to build a modular tool that others could benefit from, without being developers themselves.


Need more details ?
=========================

Please have a look at the documentation.
