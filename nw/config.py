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
        self.recentBook  = ["","","","","","","","","",""]
        
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
            if confParser.has_option(cnfSec,"winGeometry"):
                self.winGeometry = self.unpackList(
                    confParser.get(cnfSec,"winGeometry"), 2, self.winGeometry
                )
            if confParser.has_option(cnfSec,"paneSize"):
                self.paneSize = self.unpackList(
                    confParser.get(cnfSec,"paneSize"), 4, self.paneSize
                )
            if confParser.has_option(cnfSec,"theTheme"):
                self.theTheme = confParser.get(cnfSec,"theTheme")
        
        ## Editor
        cnfSec = "Editor"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"autoSave"):
                self.autoSave = confParser.getint(cnfSec,"autoSave")
            if confParser.has_option(cnfSec,"editorFont"):
                self.editorFont = confParser.get(cnfSec,"editorFont")
            if confParser.has_option(cnfSec,"lineHeight"):
                self.lineHeight = self.unpackList(
                    confParser.get(cnfSec,"lineHeight"), 2, self.lineHeight
                )
            if confParser.has_option(cnfSec,"textIndent"):
                self.textIndent = self.unpackList(
                    confParser.get(cnfSec,"textIndent"), 2, self.textIndent
                )
            if confParser.has_option(cnfSec,"parMargin"):
                self.parMargin = self.unpackList(
                    confParser.get(cnfSec,"parMargin"), 2, self.parMargin
                )
        
        ## Path
        cnfSec = "Path"
        if confParser.has_section(cnfSec):
            if confParser.has_option(cnfSec,"Recent0"):   self.recentBook[0] = confParser.get(cnfSec,"Recent0")
            if confParser.has_option(cnfSec,"Recent1"):   self.recentBook[1] = confParser.get(cnfSec,"Recent1")
            if confParser.has_option(cnfSec,"Recent2"):   self.recentBook[2] = confParser.get(cnfSec,"Recent2")
            if confParser.has_option(cnfSec,"Recent3"):   self.recentBook[3] = confParser.get(cnfSec,"Recent3")
            if confParser.has_option(cnfSec,"Recent4"):   self.recentBook[4] = confParser.get(cnfSec,"Recent4")
            if confParser.has_option(cnfSec,"Recent5"):   self.recentBook[5] = confParser.get(cnfSec,"Recent5")
            if confParser.has_option(cnfSec,"Recent6"):   self.recentBook[6] = confParser.get(cnfSec,"Recent6")
            if confParser.has_option(cnfSec,"Recent7"):   self.recentBook[7] = confParser.get(cnfSec,"Recent7")
            if confParser.has_option(cnfSec,"Recent8"):   self.recentBook[8] = confParser.get(cnfSec,"Recent8")
            if confParser.has_option(cnfSec,"Recent9"):   self.recentBook[9] = confParser.get(cnfSec,"Recent9")
        
        return
    
    def saveConfig(self):
        
        logger.debug("Config: Saving")
        confParser = configparser.ConfigParser()
        
        # Set options
        
        ## Main
        cnfSec = "Main"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"winGeometry", self.packList(self.winGeometry))
        confParser.set(cnfSec,"paneSize",    self.packList(self.paneSize))
        confParser.set(cnfSec,"thetheme",    self.theTheme)
        
        ## Editor
        cnfSec = "Editor"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"autoSave",   str(self.autoSave))
        confParser.set(cnfSec,"editorFont", str(self.editorFont))
        confParser.set(cnfSec,"lineHeight", self.packList(self.lineHeight))
        confParser.set(cnfSec,"textIndent", self.packList(self.textIndent))
        confParser.set(cnfSec,"parMargin",  self.packList(self.parMargin))
        
        ## Path
        cnfSec = "Path"
        confParser.add_section(cnfSec)
        confParser.set(cnfSec,"Recent0",    str(self.recentBook[0]))
        confParser.set(cnfSec,"Recent1",    str(self.recentBook[1]))
        confParser.set(cnfSec,"Recent2",    str(self.recentBook[2]))
        confParser.set(cnfSec,"Recent3",    str(self.recentBook[3]))
        confParser.set(cnfSec,"Recent4",    str(self.recentBook[4]))
        confParser.set(cnfSec,"Recent5",    str(self.recentBook[5]))
        confParser.set(cnfSec,"Recent6",    str(self.recentBook[6]))
        confParser.set(cnfSec,"Recent7",    str(self.recentBook[7]))
        confParser.set(cnfSec,"Recent8",    str(self.recentBook[8]))
        confParser.set(cnfSec,"Recent9",    str(self.recentBook[9]))
        
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
    
    ##
    #  GUI Actions
    ##
    
    def onLoad(self, guiObject=None):
        
        self.dlgBuilder.add_from_file(path.join(self.guiPath,"dlgPreferences.glade"))
        
        dlgPrefs = self.dlgObject("dlgPreferences")
        
        guiHandlers = {
            "onClickConfigSave"   : self.onSave,
            "onClickConfigCancel" : self.onClose,
            "onClickConfigClose"  : self.onClose,
        }
        self.dlgBuilder.connect_signals(guiHandlers)
        
        # Load Current Values
        self.dlgObject("spinFontSIze").set_value(self.fontSize)
        self.dlgObject("spinLineHeight").set_value(self.lineHeight/100.0)
        self.dlgObject("spinLineIndent").set_value(self.lineIndent/100.0)
        self.dlgObject("spinParSpacing").set_value(self.parMargin)
        self.dlgObject("spinPageMargin").set_value(self.pageMargin)
        self.dlgObject("entryLanguage").set_text(self.spellCheck)
        self.dlgObject("spinAutoSave").set_value(self.autoSave)
        self.dlgObject("spinAutoPause").set_value(self.autoPause)
        self.dlgObject("spinMinTime").set_value(self.minTime)
        
        dlgPrefs.set_transient_for(self.getObject("winMain"))
        dlgPrefs.show_all()
        
        return
    
    def onSave(self, guiObject=None):
        
        self.fontSize   = int(self.dlgObject("spinFontSIze").get_value())
        self.lineHeight = int(self.dlgObject("spinLineHeight").get_value()*100.0)
        self.lineIndent = int(self.dlgObject("spinLineIndent").get_value()*100.0)
        self.parMargin  = int(self.dlgObject("spinParSpacing").get_value())
        self.pageMargin = int(self.dlgObject("spinPageMargin").get_value())
        self.spellCheck = str(self.dlgObject("entryLanguage").get_text())
        self.autoSave   = int(self.dlgObject("spinAutoSave").get_value())
        self.autoPause  = int(self.dlgObject("spinAutoPause").get_value())
        self.minTime    = int(self.dlgObject("spinMinTime").get_value())
        
        self.saveConfig()
        dlgPrefs = self.dlgObject("dlgPreferences").destroy()
        
        return
    
    def onClose(self, guiObject=None):
        dlgPrefs = self.dlgObject("dlgPreferences").destroy()
        return
    
# End Class Config
