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
        self.htmlRoot   = "file://"+self.mainConf.guiPath.replace("\\","/")

        # Set Up Editor
        self.set_editable(False)
        self.connect("user-changed-contents",self.onContentChanged)
        self.connect("notify::load-status",self.onLoadStatusChange)
        self.load_html_string("",self.htmlRoot)
        self.fileStatus.set_from_pixbuf(getIconWidget("icon-grey",16).get_pixbuf())

        setEditor = self.get_settings()
        setEditor.set_property("enable-default-context-menu",False)
        setEditor.set_property("spell-checking-languages",self.mainConf.spellCheck)
        self.set_settings(setEditor)

        # Properties
        self.textSaved = True
        self.showPars  = False

        return

    def clearEditor(self):

        if not self.textSaved: return False

        self.load_html_string("",self.htmlRoot)
        self.fileStatus.set_from_pixbuf(getIconWidget("icon-grey",16).get_pixbuf())

        return True

    ##
    #  Loading and Saving
    ##

    def loadText(self, sceneHandle, theBook):

        self.theBook = theBook

        self.guiTimer.stopTimer()
        self.theBook.saveTiming(self.guiTimer.sessionTime)
        self.guiTimer.resetTimer()

        if not self.textSaved:
            self.saveText()

        self.theBook.loadScene(sceneHandle)
        self.theBook.setBookRecent(sceneHandle)
        self.setText(self.theBook.getSceneText())
        self.guiTimer.setPreviousTotal(self.theBook.getSceneTime())
        self.fileStatus.set_from_pixbuf(getIconWidget("icon-green",16).get_pixbuf())
        self.setEditable(False)
        self.textSaved = True
            
        return

    def saveText(self):

        if self.theBook is None: return

        scnText = self.getText()
        self.theBook.setSceneText(scnText)
        self.theBook.saveScene()
        self.fileStatus.set_from_pixbuf(getIconWidget("icon-green",16).get_pixbuf())
        self.textSaved = True

        return

    def doAutoSave(self):

        if self.theBook is None: return

        if not self.textSaved:
            logger.debug("Editor.doAutoSave: Saving")
            scnText = self.getText()
            self.theBook.setSceneText(scnText)
            self.theBook.saveScene()
            self.fileStatus.set_from_pixbuf(getIconWidget("icon-green",16).get_pixbuf())
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
        return

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):

        editState = guiObject.get_active()
        self.set_editable(editState)

        setEditor = self.get_settings()
        setEditor.set_property("enable-default-context-menu",editState)
        self.set_settings(setEditor)

        if editState:
            self.guiTimer.startTimer()
        else:
            self.guiTimer.pauseTimer()
        
        return

    def onToggleSpellCheck(self, guiObject):

        logger.debug("Editor.onToggleSpellCheck: Toggled")
        spchState = guiObject.get_active()

        setEditor = self.get_settings()
        setEditor.set_property("enable-spell-checking",spchState)
        self.set_settings(setEditor)
        
        return

    def onEditRefresh(self, guiObject):
        self.setText(self.getText())
        return

    def onEditAction(self, guiObject, theCommand):
        logger.debug("Editor.onEditAction: Action %s" % theCommand)
        self.execute_script("document.execCommand('%s',false,false);" % theCommand)
        return

    def onEditFormat(self, guiObject, theCommand):
        logger.debug("Editor.onEditFormat: Setting format %s" % theCommand)
        self.execute_script("document.execCommand('formatBlock',false,'%s');" % theCommand)
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
        logger.debug("Editor.onShowParagraphs: Toggle show paragraphs")
        self.showPars = guiObject.get_active()
        self.setText(self.getText())
        return

    def onContentChanged(self, guiObject):
        self.guiTimer.resetAutoPause()
        if self.textSaved:
            self.textSaved = False
            self.fileStatus.set_from_pixbuf(getIconWidget("icon-red",16).get_pixbuf())
        return

    def onLoadStatusChange(self, guiObject, loadStatus):
        if WebKit.LoadStatus.FINISHED:
            logger.debug("Editor.onLoadStatusChange: Loading finished")
        return

# End Class Editor
