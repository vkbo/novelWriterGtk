# -*- coding: utf-8 -*

##
#  novelWriter – Scene Summary Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the summary of the loaded scene
##

import logging as logger

from nw import *

class SceneSummary():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf   = CONFIG
        self.theOpt     = theOpt

        # Attributes
        self.summary    = ""
        self.hasSummary = False

        return

    def clearContent(self):

        # Clear Attributes
        self.summary    = ""
        self.hasSummary = False

        return

    ##
    # Load and Save
    ##

    def loadSummary(self):

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("SceneText.loadSummary: Folder not found %s" % sceneFolder)
            return

        logger.debug("SceneText.loadSummary: Loading scene summary")

        fileName  = "%s-summary-%03d.txt" % (sceneHandle,sceneVersion)
        filePath  = path.join(sceneFolder,fileName)

        if not path.isfile(filePath):
            logger.debug("SceneText.loadSummary: File not found %s" % filePath)
            return

        fileObj      = open(filePath,encoding="utf-8",mode="r")
        self.summary = fileObj.read()
        fileObj.close()

        self.hasSummary = True

        return

    def saveSummary(self):

        if not self.hasSummary:
            logger.debug("saveSummary.saveSummary: No text to save")
            return

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("saveSummary.saveSummary: Folder not found %s" % sceneFolder)
            return

        if not len(sceneHandle) == 12:
            logger.debug("saveSummary.saveSummary: Invalid scene handle '%s'" % sceneHandle)
            return

        if not sceneVersion > 0:
            logger.debug("saveSummary.saveSummary: Invalid scene version %d" % sceneVersion)
            return

        logger.debug("saveSummary.saveSummary: Saving scene text")

        fileName = "%s-summary-%03d.txt" % (sceneHandle,sceneVersion)
        filePath = path.join(sceneFolder,fileName)
        fileObj  = open(filePath,encoding="utf-8",mode="w")
        fileObj.write(self.summary)
        fileObj.close()

        return

    ##
    #  Setters
    ##

    def setSummary(self, newSummary):
        newSummary = newSummary.strip()
        if len(newSummary) > 0 and not newSummary == self.summary:
            self.summary    = newSummary
            self.hasSummary = True
        return

    ##
    #  Getters
    ##

    def getSummary(self):
        return self.summary

# End Class SceneSummary
