# -*- coding: utf-8 -*

##
#  pyÉcrire – Editor Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#  Main wrapper class for the GUI text editor.
#  This class also holds its own file DataWrapper object that contains the text of the file
#  currently being edited. This is to ensure it doesn't interfere with the editing of meta
#  data that occurs in the other tabs. That data is handled by the file object of the
#  Project class.
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")
gi.require_version("WebKit","3.0")

from gi.repository        import Gtk, Gdk, WebKit
from os                   import getcwd
from math                 import floor
from pyecrire             import *
from pyecrire.functions   import htmlStrip
from pyecrire.datawrapper import DataWrapper
from pyecrire.dialogs     import OkCancelDialog

class Editor(WebKit.WebView):

    def __init__(self, timer):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object
        self.guiTimer   = timer
        self.fileSaved  = self.getObject("imgFileSaved")

        # Paths
        self.ledGrey    = self.mainConf.guiPath+"/led-grey.png"
        self.ledGreen   = self.mainConf.guiPath+"/led-green.png"
        self.ledRed     = self.mainConf.guiPath+"/led-red.png"

        # Editor Data
        self.theFile    = DataWrapper(NAME_NONE)
        self.fileHandle = ""

        # Set Up Editor
        self.set_editable(False)
        self.connect("user-changed-contents",self.onContentChanged)
        self.load_html_string("", "file:///")
        self.fileSaved.set_from_file(self.ledGrey)

        # Formatting Menu
        fmtMenu   = Gtk.Menu()
        menuOrder = ["p","h2","h3","h4","ul","ol","pre"]
        menuItems = {
            "p"   : "Paragraph",
            "h2"  : "Large Heading",
            "h3"  : "Medium Heading",
            "h4"  : "Small Heading",
            "ul"  : "Bulleted List",
            "ol"  : "Numbered List",
            "pre" : "Preformatted",
        }

        for menuKey in menuOrder:
            fmtMenuItem = Gtk.MenuItem(menuItems[menuKey])
            fmtMenu.append(fmtMenuItem)
            fmtMenuItem.connect("activate",self.onSelectFormat, menuKey)
            fmtMenuItem.show()

        self.getObject("btnFormat").set_menu(fmtMenu)

        # Properties
        self.textSaved  = True

        return

    def clearEditor(self):

        if not self.textSaved: return False

        self.load_html_string("", "file:///")
        self.fileSaved.set_from_file(self.ledGrey)

        return True

    def updateFileDetails(self):

        fileType = self.theFile.dataType

        if fileType == NAME_PLOT or fileType == NAME_SCNE:
            self.getObject("lblBookInfoCreated").set_label(self.theFile.created)
            self.getObject("lblBookInfoUpdated").set_label(self.theFile.date)
            self.getObject("lblBookInfoVersions").set_label(str(self.theFile.listLen))
            self.getObject("lblUniverseInfoCreated").set_label("")
            self.getObject("lblUniverseInfoUpdated").set_label("")
            self.getObject("lblUniverseInfoVersions").set_label("")

        if fileType == NAME_HIST or fileType == NAME_CHAR:
            self.getObject("lblBookInfoCreated").set_label("")
            self.getObject("lblBookInfoUpdated").set_label("")
            self.getObject("lblBookInfoVersions").set_label("")
            self.getObject("lblUniverseInfoCreated").set_label(self.theFile.created)
            self.getObject("lblUniverseInfoUpdated").set_label(self.theFile.date)
            self.getObject("lblUniverseInfoVersions").set_label(str(self.theFile.listLen))

        return

    ##
    #  Load and Save
    ##

    def loadFile(self, fileType, filePath, fileHandle, doWordCount=True):

        logger.debug("Loading file")

        if not self.textSaved:
            self.theFile.doAutoSaveText()

        self.onTimerStop()
        self.setEditable(False)
        self.guiTimer.resetTimer()
        self.guiTimer.resetAutoPause()

        self.theFile    = DataWrapper(NAME_NONE)
        self.fileHandle = fileHandle
        self.textSaved  = True

        self.theFile.setDataPath(filePath)
        self.theFile.setDataType(fileType)
        self.theFile.loadDetails()
        self.theFile.loadText()
        self.theFile.loadTiming()
        self.guiTimer.setDocTotal(self.theFile.timeTotal)

        if doWordCount:
            self.theFile.prevWords = self.theFile.words
            self.theFile.prevChars = self.theFile.chars

        self.setText(self.theFile.text)
        self.updateFileDetails()

        return

    def loadFileVersion(self, filePath):

        self.theFile.setFileToLoad(filePath)
        self.theFile.loadText()
        self.setText(self.theFile.text)

        return

    def saveFile(self):

        srcText = self.getText()

        self.theFile.setText(srcText)
        self.theFile.saveText()

        self.textSaved = True
        self.fileSaved.set_from_file(self.ledGreen)

        return

    def doAutoSave(self):

        srcText = self.getText()

        self.theFile.setText(srcText)
        self.theFile.doAutoSaveText()

        self.textSaved = True
        self.fileSaved.set_from_file(self.ledGreen)

        return True

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):
        self.setEditable(guiObject.get_active(),"Button")
        return

    def onSelectFormat(self, guiObject, fmtCode):
        logger.debug("Set format to %s" % fmtCode)
        if   fmtCode == "ol":
            self.execute_script("document.execCommand('insertOrderedList',false,false);")
        elif fmtCode == "ul":
            self.execute_script("document.execCommand('insertUnorderedList',false,false);")
        else:
            self.execute_script("document.execCommand('formatBlock',false,'%s');" % fmtCode)
        return

    def onEditAction(self, guiObject):
        logger.debug("Editor action %s" % guiObject.get_name())
        self.execute_script("document.execCommand('%s',false,false);" % guiObject.get_name())
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

    def onEditStripFormatting(self, guiObject):
        guiDialog = OkCancelDialog("Clear all document formatting?")
        if guiDialog.run() == Gtk.ResponseType.OK:
            srcText = self.getText()
            srcText = htmlStrip(srcText)
            self.setText(srcText)
        guiDialog.destroy()
        return

    def onContentChanged(self, guiObject):

        if self.textSaved:
            self.textSaved = False
            self.fileSaved.set_from_file(self.ledRed)

        # Reset timer auto-pause
        self.guiTimer.resetAutoPause()

        return

    def onTimerStart(self, guiObject=None):
        self.guiTimer.startTimer()
        return

    def onTimerPause(self, guiObject=None):
        self.guiTimer.pauseTimer()
        return

    def onTimerStop(self, guiObject=None):
        self.guiTimer.stopTimer()
        self.theFile.setText(self.getText())
        self.theFile.saveTiming(self.guiTimer.currTime)
        self.guiTimer.setDocTotal(self.theFile.timeTotal)
        self.setEditable(False)
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

        fontSize   = str(self.mainConf.fontSize)
        lineHeight = str(self.mainConf.lineHeight/100.0)
        lineIndent = str(self.mainConf.lineIndent/100.0)
        parMargin  = str(self.mainConf.parMargin)

        if self.theFile.editFormat.lower() == "indent": parMargin  = "0"
        if self.theFile.editFormat.lower() == "skip":   lineIndent = "0"

        srcHtml  = "<html>"
        srcHtml += "<head>"
        srcHtml += "  <style>"
        srcHtml += "    body {font-size: "+fontSize+"px; padding: 40px; line-height: "+lineHeight+"em;}"
        srcHtml += "    h2   {margin: 0 0 0.7em 0; font-size: 1.6em;}"
        srcHtml += "    h3   {margin: 0 0 0.5em 0; font-size: 1.4em;}"
        srcHtml += "    h4   {margin: 0 0 0.5em 0; font-size: 1.2em;}"
        srcHtml += "    li   {text-align: justify;}"
        srcHtml += "    p    {margin: "+parMargin+"px 0; text-align: justify;}"
        srcHtml += "    p+p  {text-indent: "+lineIndent+"em;}"
        srcHtml += "  </style>"
        srcHtml += "</head>"
        srcHtml += "<body>"+srcText+"</body>"
        srcHtml += "</html>"

        self.load_html_string(srcHtml,"file:///")

        return True

    def setEditable(self, makeEditable, initSource="Action"):

        if initSource != "Button":
            self.getObject("btnEditFile").set_active(makeEditable)
        self.set_editable(makeEditable)

        if makeEditable:
            self.guiTimer.startTimer()
        else:
            self.guiTimer.pauseTimer()

        return

# End Class Editor
