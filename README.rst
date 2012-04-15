===================================
Presentation of the Santoku project
===================================

Santoku is a utility designed to generate configuration files for Shinken and Nagios from data provided in a CSV file. The CSV file is expected to have a specific format (described in the doc... later ;-).
The generated files are :
- hosts.cfg, including host groups (done !)
- services.cfg (on going)
- commands.cfg (0% done)
- and a very basic tabular-presented Nagvis map showing ALL hosts listed in the CSV file (0% done)

At a previous position, I wrote a PERL script doing all this (except the commands.cfg part). This script still works very well, but because of the numerous plugins / environments / usages it handles, it's now a 50KBytes cluttered script and debugging/updating it has become a nightmare. So I can't even share it with the community.
This is why I started developping Santoku : I'd like to build a modular tool that others could benefit from, without being developers themselves.


How to install Santoku
=========================

(todo)


How to update
=========================

(todo)


Requirements
=========================

Python 2.6 or higher.


How to run Santoku ?
================================

1. Set up Santoku options (in still-to-come config file)
2. Define source data in CSV format using LibreOffice Calc or MS-Excel
3. Define plugin and related module
4. Run santoku !

(lots of details to come)


FAQ
========================

Why "Santoku ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Well, ... there was Batman and Robin. Now, there is Shinken and Santoku :-)
Actually, since Santoku is designed to be used together with Shinken, I wanted to name it as a Japanese cutting device. However, since Santoku is a very humble piece of software, I could not name it as a deadly weapon :  `a santoku is a japanese kitchen knife <https://en.wikipedia.org/wiki/Santoku>`_.

Who is "Santoku" for ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is for anybody willing to automate the creation of Shinken/Nagios configuration files, especially if the monitored devices/hosts are already listed in a database.



Known bugs
================================

This is still in development, so expect a lot !

