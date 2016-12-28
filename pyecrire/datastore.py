# -*- coding: utf-8 -*

import logging as logger
import configparser

from os import path

class DataWrapper():

    def __init__(self, dataType):

        # Constants
        self.TYPE_BOOK     = "Book"
        self.PREF_BOOK     = "B"
        self.TYPE_UNIVERSE = "Universe"
        self.PREF_UNIVERSE = "U"

        # Default Values
        self.dataType = dataType
        self.dataPath = ""
        self.title    = ""
        self.created  = 0
        self.date     = 0
        self.notes    = ""
        self.hasNotes = False
        self.text     = ""
        self.hasText  = False
        self.words    = 0

        return


    def saveDetails(self):

        logger.debug("Saving data details")
        confParser = configparser.ConfigParser()

        # Set Variables
        cnfSec = self.dataType
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Title",  str(self.title))
        confParser.set(cnfSec,"Created",str(self.created))
        confParser.set(cnfSec,"Date",   str(self.date))
        confParser.set(cnfSec,"Notes",  str(self.hasNotes))
        confParser.set(cnfSec,"Text",   str(self.hasText))
        confParser.set(cnfSec,"Words",  str(self.words))

        # Write File
        confParser.write(open(path.join(self.dataPath,"details.txt"),"w"))

        return


    ##
    #  Setters
    ##

    def setTitle(self, newTitle):
        if len(newTitle) > 0:
            self.title = newTitle
        else:
            logger.error("Setting %s title failed." % lower(self.dataType))
        return

    def setDataPath(self, newPath):
        if path.isdir(newPath):
            self.dataPath = newPath
        else:
            logger.error("Path not found: %s" % newPath)
        return

# End Class DataWrapper

