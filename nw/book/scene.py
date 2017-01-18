# -*- coding: utf-8 -*

##
#  novelWriter – Scene Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the scene of the loaded book
##

import logging as logger

from os                   import listdir
# from time                 import time
# from hashlib              import sha256
from nw                   import *
from nw.book.sceneopt     import SceneOpt
from nw.book.scenemeta    import SceneMeta
from nw.book.scenetext    import SceneText
from nw.book.scenesummary import SceneSummary
from nw.book.scenetiming  import SceneTiming

class Scene():

    def __init__(self, bookOpt, sceneHandle):

        # Core Objects
        self.mainConf    = CONFIG
        self.theOpt      = SceneOpt()
        self.theMeta     = SceneMeta(self.theOpt)
        self.theText     = SceneText(self.theOpt)
        self.theSummary  = SceneSummary(self.theOpt)
        self.theTiming   = SceneTiming(self.theOpt,self.theText)

        # Runtime Attributes
        self.sceneLoaded = False
        self.readOnly    = False

        # Set Options
        self.theOpt.setSceneHandle(sceneHandle)
        self.theOpt.setSceneFolder(bookOpt.getSceneFolder())

        # Connect Functions

        ## Setters

        ## Getters
        self.getTitle   = self.theMeta.getTitle
        self.getCreated = self.theMeta.getCreated
        self.getUpdated = self.theMeta.getUpdated
        self.getSection = self.theMeta.getSection
        self.getChapter = self.theMeta.getChapter
        self.getNumber  = self.theMeta.getNumber
        self.getWords   = self.theMeta.getWords
        self.getChars   = self.theMeta.getChars
        self.getChanged = self.theMeta.getChanged

        return

    ##
    #  Create, Load and Save
    ##

    def loadScene(self, metaOnly=False, readOnly=False):

        self.theMeta.loadData()
        if not metaOnly:
            self.theText.loadText()
            self.theSummary.loadSummary()
            self.theTiming.loadTiming()

        self.readOnly = readOnly

        return

    def saveScene(self, saveAll=False):

        if self.readOnly:
            logger.debug("Scene.saveScene: Scene is read only. Skipping")
            return

        self.theMeta.setUpdated(formatDateTime())
        self.theMeta.setWords(self.theText.wordsLatest)
        self.theMeta.setChars(self.theText.charsLatest)

        self.theMeta.saveData()
        self.theText.saveText()
        self.theSummary.saveSummary()

        if saveAll:
            self.theTiming.saveTiming()

        return

# End Class Scene
