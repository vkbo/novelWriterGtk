# -*- coding: utf-8 -*

##
#  novelWriter – Editor Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Main wrapper class for the GUI text editor.
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")
gi.require_version("WebKit","3.0")

from gi.repository import Gtk, WebKit
from nw            import *

class Editor(WebKit.WebView):

    def __init__(self, timer):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object
        self.guiTimer   = timer
        self.theBook    = None
        self.fileStatus = self.getObject("imgStatusFile")
        self.lblStatus  = self.getObject("lblStatusFile")

        # Paths
        self.ledGrey    = self.mainConf.guiPath+"/led-grey.png"
        self.ledGreen   = self.mainConf.guiPath+"/led-green.png"
        self.ledRed     = self.mainConf.guiPath+"/led-red.png"
        self.htmlRoot   = "file://"+self.mainConf.guiPath.replace("\\","/")

        # Set Up Editor
        self.set_editable(False)
        self.connect("user-changed-contents",self.onContentChanged)
        self.load_html_string("",self.htmlRoot)
        self.fileStatus.set_from_file(self.ledGrey)

        # Properties
        self.textSaved  = True
        self.showPars   = False

        return

    def clearEditor(self):

        if not self.textSaved: return False

        self.load_html_string("",self.htmlRoot)
        self.fileStatus.set_from_file(self.ledGrey)

        return True

    ##
    #  Loading and Saving
    ##

    def loadText(self, fileHandle, theBook):

        self.theBook = theBook

        self.guiTimer.stopTimer()
        self.theBook.theScene.saveTiming(self.guiTimer.sessionTime)
        self.guiTimer.resetTimer()

        if not self.textSaved:
            self.saveText()

        self.theBook.loadScene(fileHandle)
        self.setText(self.theBook.getText())
        self.guiTimer.setPreviousTotal(self.theBook.theScene.timeTotal)
        self.fileStatus.set_from_file(self.ledGreen)
        self.setEditable(False)
        self.textSaved = True
            
        return

    def saveText(self):

        scnText = self.getText()
        self.theBook.theScene.setText(scnText)
        self.theBook.saveScene()
        self.fileStatus.set_from_file(self.ledGreen)
        self.textSaved = True

        return

    def doAutoSave(self):

        if not self.textSaved:
            logger.debug("Editor: Autsaving")
            scnText = self.getText()
            self.theBook.theScene.setText(scnText)
            self.theBook.doAutoSave()
            self.fileStatus.set_from_file(self.ledGreen)
            self.textSaved = True
            
        return

    ##
    #  Getters
    ##

    def getText(self):

        self.execute_script("document.title=document.documentElement.innerHTML;")
        srcHtml = self.get_main_frame().get_title()

        bodyStart = srcHtml.find("<body")
        bodyStart = srcHtml.find(">",bodyStart)+1
        bodyEnd   = srcHtml.find("</body>")

        return srcHtml[bodyStart:bodyEnd]

    ##
    #  Setters
    ##

    def setText(self, srcText):

        if not self.textSaved: return False

        fontSize   = self.mainConf.fontSize
        lineHeight = self.mainConf.lineHeight/100.0
        lineIndent = self.mainConf.lineIndent/100.0
        parMargin  = self.mainConf.parMargin
        pageMargin = self.mainConf.pageMargin

        cssPath   = path.join(self.mainConf.guiPath,"editor.css")
        fileObj   = open(cssPath,"r")
        cssStyles = fileObj.read()
        fileObj.close()

        if self.showPars: parMargin -= 1

        cssStyles = cssStyles.replace("%fontSize%",str(fontSize))
        cssStyles = cssStyles.replace("%lineHeight%",str(lineHeight))
        cssStyles = cssStyles.replace("%lineIndent%",str(lineIndent))
        cssStyles = cssStyles.replace("%parMargin%",str(parMargin))
        cssStyles = cssStyles.replace("%pageMargin%",str(pageMargin))

        if self.showPars:
            cssStyles += "\n"
            cssStyles += "p {border: 1px dashed #aaaaaa;}\n"

        srcHtml  = "<html>"
        srcHtml += "<head>"
        srcHtml += "<style>"
        srcHtml += cssStyles
        srcHtml += "</style>"
        srcHtml += "</head>"
        srcHtml += "<body>"+srcText+"</body>"
        srcHtml += "</html>"

        self.load_html_string(srcHtml,self.htmlRoot)
        self.setEditable(False)

        return True

    def setEditable(self, editState):
        self.getObject("btnEditable").set_active(editState)
        #self.set_editable(editState)
        return

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):

        editState = guiObject.get_active()
        self.set_editable(editState)

        if editState:
            self.guiTimer.startTimer()
        else:
            self.guiTimer.pauseTimer()
        
        return

    def onEditRefresh(self, guiObject):
        self.setText(self.getText())
        return

    def onEditAction(self, guiObject, theCommand):
        logger.debug("Editor: Action %s" % theCommand)
        self.execute_script("document.execCommand('%s',false,false);" % theCommand)
        return

    def onEditCopy(self, guiObject):
        self.copy_clipboard()
        return

    def onEditCut(self, guiObject):
        self.cut_clipboard()
        return

    def onEditPaste(self, guiObject):
        self.paste_clipboard()
        return

    def onShowParagraphs(self, guiObject):
        logger.debug("Editor: Toggle show paragraphs")
        self.showPars = guiObject.get_active()
        self.setText(self.getText())
        return

    def onContentChanged(self, guiObject):
        self.guiTimer.resetAutoPause()
        if self.textSaved:
            self.textSaved = False
            self.fileStatus.set_from_file(self.ledRed)
        return

# End Class Editor
