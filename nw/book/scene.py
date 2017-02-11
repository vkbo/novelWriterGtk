# -*- coding: utf-8 -*

##
#  novelWriter – Scene Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the scene of the loaded book
##

import logging as logger

from os                   import listdir
from time                 import time
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
        self.openTime    = time()

        # Set Options
        self.theOpt.setSceneHandle(sceneHandle)
        self.theOpt.setSceneFolder(bookOpt.getSceneFolder())

        # Connect Functions

        ## Load and Save
        self.loadTiming   = self.theTiming.loadTiming
        self.saveTiming   = self.theTiming.saveTiming

        ## Setters
        self.setTitle     = self.theMeta.setTitle
        self.setSection   = self.theMeta.setSection
        self.setChapter   = self.theMeta.setChapter
        self.setNumber    = self.theMeta.setNumber
        self.setText      = self.theText.setText
        self.setSummary   = self.theSummary.setSummary
        self.setTime      = self.theTiming.setTime

        ## Getters
        self.getHandle    = self.theOpt.getSceneHandle
        self.getVersion   = self.theOpt.getSceneVersion
        self.getTitle     = self.theMeta.getTitle
        self.getCreated   = self.theMeta.getCreated
        self.getUpdated   = self.theMeta.getUpdated
        self.getSection   = self.theMeta.getSection
        self.getChapter   = self.theMeta.getChapter
        self.getNumber    = self.theMeta.getNumber
        self.getWords     = self.theMeta.getWords
        self.getChars     = self.theMeta.getChars
        self.getMetaTime  = self.theMeta.getTime
        self.getChanged   = self.theMeta.getChanged
        self.getText      = self.theText.getText
        self.getWordCount = self.theText.getWordCount
        self.getCharCount = self.theText.getCharCount
        self.getSummary   = self.theSummary.getSummary
        self.getTimeTotal = self.theTiming.getTimeTotal
        self.getTimeList  = self.theTiming.getTimeList

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
            logger.debug("Scene.saveScene: Scene is read only")
            return

        textSaved    = self.theText.saveText()
        summarySaved = self.theSummary.saveSummary()

        if textSaved or summarySaved:
            self.theMeta.setUpdated(formatDateTime())

        self.theMeta.setWords(self.theText.wordsLatest)
        self.theMeta.setChars(self.theText.charsLatest)
        self.theMeta.setTime(self.theTiming.timeCurrent)

        self.theMeta.saveData()

        if saveAll:
            self.theTiming.saveTiming()

        return

    ##
    #  Getters
    ##

    def getOpenTime(self):
        return self.openTime

    ##
    #  Other Actions
    ##

    def resetOpenTime(self):
        self.openTime = time()
        return

    ##
    #  Events
    ##

    def onAutoSave(self):

        logger.debug("Scene.onAutoSave: Autosave")
        self.saveScene(False)
        self.theTiming.saveTiming(True)

        return

# End Class Scene
