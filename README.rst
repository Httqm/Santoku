===================================
Presentation of the Santoku project
===================================

Santoku is a utility designed to generate configuration files for Shinken and Nagios from data provided in a CSV file. The CSV file is expected to have a specific format (described in the documentation).
The generated files are :

- hosts.cfg, including host groups and service groups
- services.cfg
- commands.cfg
- and a very basic tabular-presented Nagvis map showing ALL hosts listed in the CSV file (not done yet)


Setup :
=========================
1. git clone https://github.com/Httqm/Santoku.git
2. copy ./deployToShinken.sh-dist into deployToShinken.sh
3. copy modules/config.py-dist into modules/config.py
4. create the ./output folder (if not already there)


Need more details ?
=========================

Please have a look at "doc/documentation.html".
