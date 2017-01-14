# -*- coding: utf-8 -*

##
#  novelWriter – Scene Text Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Holds the text of the loaded scene
##

import logging as logger

from os      import path
from hashlib import sha256
from re      import sub
from bleach  import clean
from html    import unescape
from nw      import *

class SceneText():

    def __init__(self, theOpt):

        # Core Objects
        self.mainConf    = CONFIG
        self.theOpt      = theOpt

        # Attributes
        self.text        = ""
        self.textHash    = ""
        self.hasText     = False
        self.wordsOnLoad = 0
        self.charsOnLoad = 0
        self.wordsAdded  = 0
        self.charsAdded  = 0
        self.wordsLatest = 0
        self.charsLatest = 0

        return

    def clearContent(self):

        # Clear Attributes
        self.text        = ""
        self.textHash    = ""
        self.hasText     = False
        self.wordsOnLoad = 0
        self.charsOnLoad = 0
        self.wordsAdded  = 0
        self.charsAdded  = 0
        self.wordsLatest = 0
        self.charsLatest = 0

        return

    ##
    #  Load and Save
    ##

    def loadText(self):

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("SceneText.loadText: Folder not found %s" % sceneFolder)
            return

        logger.debug("SceneText.loadText: Loading scene text")

        fileName  = "%s-scene-%03d.txt" % (sceneHandle,sceneVersion)
        filePath  = path.join(sceneFolder,fileName)

        if not path.isfile(filePath):
            logger.debug("SceneText.loadText: File not found %s" % filePath)
            return

        fileObj   = open(filePath,encoding="utf-8",mode="r")
        self.text = fileObj.read()
        fileObj.close()

        words, chars     = self.countWords(self.text)
        self.wordsOnLoad = words
        self.charsOnLoad = chars
        self.wordsLatest = words
        self.charsLatest = chars
        self.textHash    = sha256(str(self.text).encode()).hexdigest()
        self.hasText     = True

        return

    def saveText(self):

        if not self.hasText:
            logger.debug("SceneText.saveText: No text to save")
            return

        sceneFolder  = self.theOpt.sceneFolder
        sceneHandle  = self.theOpt.sceneHandle
        sceneVersion = self.theOpt.sceneVersion

        if not path.isdir(sceneFolder):
            logger.debug("SceneText.saveText: Folder not found %s" % sceneFolder)
            return

        logger.debug("SceneText.saveText: Saving scene text")

        fileName = "%s-scene-%03d.txt" % (sceneHandle,sceneVersion)
        filePath = path.join(sceneFolder,fileName)
        fileObj  = open(filePath,encoding="utf-8",mode="w")
        fileObj.write(self.text)
        fileObj.close()

        words, chars     = self.countWords(self.text)
        self.wordsLatest = words
        self.charsLatest = chars
        self.textHash    = sha256(str(self.text).encode()).hexdigest()

        return

    ##
    #  Setters
    ##

    def setText(self, srcText):
        if len(srcText) > 0:
            srcText          = self.htmlCleanUp(srcText)
            self.text        = srcText
            self.hasText     = True
            words,chars      = self.countWords(srcText)
            self.wordsAdded  = words - self.wordsOnLoad
            self.charsAdded  = chars - self.charsOnLoad
            self.wordsLatest = words
            self.charsLatest = chars
        return

    ##
    #  Getters
    ##

    def getText(self):
        return self.text

    ##
    #  Methods
    ##

    def countWords(self, srcText):

        cleanText = srcText.strip()
        cleanText = sub("<.*?>"," ",cleanText)
        cleanText = sub("&.*?;","?",cleanText)
        cleanText = cleanText.strip()
        splitText = cleanText.split()

        return len(splitText), len(cleanText)

    def htmlCleanUp(self, srcText):

        okTags   = ["p","b","i","u","strike","ul","ol","li","h2","h3","h4","pre"]
        okAttr   = {"*" : ["style"]}
        okStyles = ["text-align"]

        srcText  = clean(srcText,tags=okTags,attributes=okAttr,styles=okStyles,strip=True)

        if srcText[0:3] != "<p>": srcText = "<p>"+srcText+"</p>"

        srcText = unescape(srcText)
        srcText = srcText.replace("</p> ","</p>")
        srcText = srcText.replace("<p></p>","")
        srcText = srcText.replace("</p>","</p>\n")
        srcText = srcText.replace('style=""',"")
        srcText = srcText.replace("style=''","")
        srcText = srcText.replace(" >",">")
        srcText = srcText.replace("\u00A0"," ")
        srcText = srcText.replace("\n ","\n")

        return srcText

# End Class SceneText
