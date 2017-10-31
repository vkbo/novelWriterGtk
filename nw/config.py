# -*- coding: utf-8 -*
"""novelWriter Config Class

 novelWriter – Config Class
============================
 This class reads and store the main preferences of the application

 File History:
 Created: 2017-01-10 [0.1.0]

"""

import logging
import configparser
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path, mkdir, getcwd
from appdirs       import user_config_dir

logger = logging.getLogger(__name__)

class Config:
    
    WIN_WIDTH  = 0
    WIN_HEIGHT = 1
    
    PANE_MAIN  = 0
    PANE_CONT  = 1
    PANE_EDIT  = 2
    PANE_META  = 3
    
    FILE_SCENE = 0
    FILE_NOTE  = 1
    
    def __init__(self):
        
        # Core Settings
        self.guiState   = True
        
        # Set Application Variables
        self.appName    = "novelWriter"
        self.appHandle  = "novelwriter"
        self.appURL     = "https://github.com/vkbo/novelWriter"
        
        # Set Paths
        self.confPath   = user_config_dir(self.appHandle)
        self.confFile   = self.appHandle+".conf"
        self.homePath   = path.expanduser("~")
        self.appPath    = path.dirname(__file__)
        self.guiPath    = path.join(self.appPath,"gui")
        self.themePath  = path.join(self.appPath,"themes")
        
        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        # TODO: This does not work on Windows
        if not path.isdir(self.confPath):
            mkdir(self.confPath)
            
        # Set default values
        self.confChanged = False
        
        ## General
        self.winGeometry = [1600, 980]
        self.paneSize    = [280, 750, 900, 240]
        self.theTheme    = "default"
        
        ## Editor
        self.autoSave    = 300         # Seconds
        self.editorFont  = "Tinos 15"  # FontName + fontSize
        self.lineHeight  = [120,120]   # Percent
        self.textIndent  = [30, 0]     # Pixels
        self.parMargin   = [4, 12]     # Pixels
        self.spellCheck  = "en_GB"
        self.spellState  = False
        
        ## Paths
        self.recentBook  = [""]*10
        
        # Check if config file exists
        if path.isfile(path.join(self.confPath,self.confFile)):
            self.loadConfig()
            
        # Save a copy of the default config if no file exists
        if not path.isfile(path.join(self.confPath,self.confFile)):
            self.saveConfig()
            
        return
    
    ##
    #  Actions
    ##
    
    def loadConfig(self):
        
        logger.debug("Loading config file")
        confParser = configparser.ConfigParser()
        confParser.readfp(open(path.join(self.confPath,self.confFile)))
        
        # Get options
        
        ## Main
        cnfSec = "Main"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"geometry"):
                self.winGeometry = self.unpackList(
                    confParser.get(cnfSec,"geometry"), 2, self.winGeometry
                )
            if confParser.has_option(cnfSec,"panes"):
                self.paneSize = self.unpackList(
                    confParser.get(cnfSec,"panes"), 4, self.paneSize
                )
            if confParser.has_option(cnfSec,"theme"):
                self.theTheme = confParser.get(cnfSec,"theme")
        
        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autosave"):
                self.autoSave = confParser.getint(cnfSec,"autosave")
            if confParser.has_option(cnfSec,"font"):
                self.editorFont = confParser.get(cnfSec,"font")
            if confParser.has_option(cnfSec,"lineheight"):
                self.lineHeight = self.unpackList(
                    confParser.get(cnfSec,"lineheight"), 2, self.lineHeight
                )
            if confParser.has_option(cnfSec,"textindent"):
                self.textIndent = self.unpackList(
                    confParser.get(cnfSec,"textindent"), 2, self.textIndent
                )
            if confParser.has_option(cnfSec,"parmargin"):
                self.parMargin = self.unpackList(
                    confParser.get(cnfSec,"parmargin"), 2, self.parMargin
                )
        
        ## Path
        cnfSec = "Path"
        if confParser.has_section(cnfSec):
            for i in range(10):
                if confParser.has_option(cnfSec,"recent%d" % i):
                    self.recentBook[i] = confParser.get(cnfSec,"recent%d" % i)
        
        return
    
    def saveConfig(self):
        
        logger.debug("Config: Saving")
        confParser = configparser.ConfigParser()
        
        # Set options
        
        ## Main
        cnfSec = "Main"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"geometry", self.packList(self.winGeometry))
        confParser.set(cnfSec,"panes",    self.packList(self.paneSize))
        confParser.set(cnfSec,"theme",    self.theTheme)
        
        ## Editor
        cnfSec = "Editor"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"autosave",   str(self.autoSave))
        confParser.set(cnfSec,"font",       str(self.editorFont))
        confParser.set(cnfSec,"lineheight", self.packList(self.lineHeight))
        confParser.set(cnfSec,"textindent", self.packList(self.textIndent))
        confParser.set(cnfSec,"parmargin",  self.packList(self.parMargin))
        
        ## Path
        cnfSec = "Path"
        confParser.add_section(cnfSec)
        for i in range(10):
            confParser.set(cnfSec,"recent%d" % i, str(self.recentBook[i]))
        
        # Write config file
        confParser.write(open(path.join(self.confPath,self.confFile),"w"))
        self.confChanged = False
        
        return
    
    def unpackList(self, inStr, listLen, listDefault, castTo=int):
        inData  = inStr.split(",")
        outData = []
        for i in range(listLen):
            try:
                outData.append(castTo(inData[i]))
            except:
                outData.append(listDefault[i])
        return outData
    
    def packList(self, inData):
        return ", ".join(str(inVal) for inVal in inData)
    
    ##
    #  Events
    ##
    
    def onAutoSave(self):
        if self.confChanged:
            logger.debug("Config: Autosaving")
            self.saveConfig()
        return True
    
    ##
    #  Setters
    ##
    
    def setConfPath(self, newPath):
        if newPath is None: return
        if not path.isfile(newPath):
            logger.error("Config: File not found. Using default config path instead.")
            return
        self.confPath = path.dirname(newPath)
        self.confFile = path.basename(newPath)
        return
    
    def setGUIState(self, guiState):
        self.guiState = guiState
        return
    
    def setWinSize(self, newWidth, newHeight):
        if abs(self.winGeometry[self.WIN_WIDTH] - newWidth) >= 10:
            self.winGeometry[self.WIN_WIDTH] = newWidth
            self.confChanged = True
        if abs(self.winGeometry[self.WIN_HEIGHT] - newHeight) >= 10:
            self.winGeometry[self.WIN_HEIGHT] = newHeight
            self.confChanged = True
        return
    
    def setPanePosition(self, panePos, whichOne):
        if panePos != self.paneSize[whichOne]:
            self.paneSize[whichOne] = panePos
            self.confChanged = True
        return
    
    def setSpellState(self, state):
        self.spellState = state
        return
    
    def setLastBook(self, bookPath):
        if bookPath == "": return
        if bookPath in self.recentBook[0:10]:
            self.recentBook.remove(bookPath)
        self.recentBook.insert(0,bookPath)
        self.confChanged = True
        self.updateRecentList()
        return
    
    ##
    #  Getters
    ##
    
    def getLastBook(self, bookIdx=0):
        return self.recentBook[bookIdx]
    
    ##
    #  Methods
    ##
    
    def updateRecentList(self):
        # for n in range(10):
        #     if self.recentBook[n] == "":
        #         self.getObject("menuFileRecent%d" % n).set_visible(False)
        #     else:
        #         self.getObject("menuFileRecent%d" % n).set_visible(True)
        #         self.getObject("menuFileRecent%d" % n).set_label(self.recentBook[n])
        return
    
# End Class Config
