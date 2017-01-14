# -*- coding: utf-8 -*

##
#  novelWriter – Scene Meta Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the metadata of the loaded scene
##

import logging as logger
import configparser

from time    import time
from nw      import *

class SceneMeta():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf     = CONFIG
        self.theOpt       = theOpt

        # Saved Attributes
        self.sceneTitle   = ""
        self.sceneCreated = formatDateTime()
        self.sceneUpdated = formatDateTime()
        self.sceneSection = 0
        self.sceneChapter = 1
        self.sceneNumber  = 1
        self.sceneWords   = 0
        self.sceneChars   = 0

        return

    def clearContent(self):

        # Clear Saved Attributes
        self.sceneTitle   = ""
        self.sceneCreated = formatDateTime()
        self.sceneUpdated = formatDateTime()
        self.sceneSection = 0
        self.sceneChapter = 1
        self.sceneNumber  = 1
        self.sceneWords   = 0
        self.sceneChars   = 0

        return

    ##
    #  Load and Save
    ##

    def loadData(self, sceneHandle):

        sceneFolder = self.theOpt.sceneFolder

        if sceneHandle == "" or sceneHandle is None:
            logger.error("SceneMeta.loadData: File handle missing")
            return

        self.sceneHandle = sceneHandle

        fileName = "%s-metadata.cnf" % self.sceneHandle
        filePath = path.join(sceneFolder,fileName)

        if not path.isfile(filePath):
            logger.error("SceneMeta.loadData: File not found %s" % filePath)
            return

        logger.debug("SceneMeta.loadData: Loading scene metadata")

        confParser = configparser.ConfigParser()
        confParser.readfp(open(filePath,"r"))

        # Get Variables
        cnfSec = "Scene"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Title"):   self.sceneTitle   = confParser.get(cnfSec,"Title")
            if confParser.has_option(cnfSec,"Created"): self.sceneCreated = confParser.get(cnfSec,"Created")
            if confParser.has_option(cnfSec,"Updated"): self.sceneUpdated = confParser.get(cnfSec,"Updated")
            if confParser.has_option(cnfSec,"Section"): self.sceneSection = confParser.getint(cnfSec,"Section")
            if confParser.has_option(cnfSec,"Chapter"): self.sceneChapter = confParser.getint(cnfSec,"Chapter")
            if confParser.has_option(cnfSec,"Number"):  self.sceneNumber  = confParser.getint(cnfSec,"Number")
            if confParser.has_option(cnfSec,"Words"):   self.sceneWords   = confParser.getint(cnfSec,"Words")
            if confParser.has_option(cnfSec,"Chars"):   self.sceneChars   = confParser.getint(cnfSec,"Chars")

        return

# End Class SceneMeta
