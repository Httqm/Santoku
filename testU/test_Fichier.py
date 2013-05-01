#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest


########################################## ##########################################################
# allows importing from parent folder
# source : http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
########################################## ##########################################################


from modules import debug
from modules import Fichier
import os

debug = debug.Debug()

class test_Fichier(unittest.TestCase):

    def test1_openValidUtf8File(self):
        """
        Try to open a valid UTF-8 file.
        Everything should be fine.
        """
        testFile = open('./validUtf8File','w')
        testFile.write('Klüft skräms inför på fédéral électoral große')
        testFile.close()

        try:
            myCsvFile = Fichier.FileCsv(testFile.name)
        except:
            pass

        os.remove(testFile.name)
        self.assertIs(type(myCsvFile), Fichier.FileCsv, 'Failed opening a valid UTF-8. This is a BUG !')


    def test2_openInvalidUtf8File(self):
        """
        Open an ISO-8859-1 file while expecting a UTF-8 file
        Should detect it and complain loudly !
        """
        # open the file in binary mode to avoid 'TypeError: must be str, not bytes' error.
        testFile = open('./invalidUtf8File','wb')
        # available encodings : http://docs.python.org/2/library/codecs.html#standard-encodings
        testFile.write('Klüft skräms inför på fédéral électoral große'.encode('latin_1', 'strict'))
        testFile.close()

        myCsvFile = None
        try:
            myCsvFile = Fichier.FileCsv(testFile.name)
        except:
            debug.show('Successfully detected non-UTF-8 file.')

        os.remove(testFile.name)
        self.assertIsNot(type(myCsvFile), Fichier.FileCsv)
