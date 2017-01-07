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

class Editor(WebKit.WebView):

    def __init__(self):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object
        self.fileSaved  = self.getObject("imgFileSaved")

        # Paths
        self.ledGrey    = self.mainConf.guiPath+"/led-grey.png"
        self.ledGreen   = self.mainConf.guiPath+"/led-green.png"
        self.ledRed     = self.mainConf.guiPath+"/led-red.png"

        # Editor Data
        self.theFile    = DataWrapper(NAME_NONE)
        self.fileHandle = ""
        self.startWords = 0
        self.startChars = 0

        # Set Up Editor
        self.set_editable(False)
        self.connect("key_press_event",self.onEventKeyPress)
        self.connect("user-changed-contents",self.onContentChanged)
        self.load_html_string("", "file:///")
        self.fileSaved.set_from_file(self.ledGrey)

        # Properties
        self.textSaved  = True

        return

    def clearEditor(self):

        if not self.textSaved: return False

        self.load_html_string("", "file:///")
        self.fileSaved.set_from_file(self.ledGrey)

        return True

    def loadFile(self, fileType, filePath, fileHandle, doWordCount=True):

        logger.debug("Loading file")

        if not self.textSaved:
            self.theFile.autoSaveText()

        self.theFile    = DataWrapper(NAME_NONE)
        self.fileHandle = fileHandle
        self.textSaved  = True

        self.theFile.setDataPath(filePath)
        self.theFile.setDataType(fileType)
        self.theFile.loadDetails()
        self.theFile.loadText()

        if doWordCount:
            self.startWords = self.theFile.words
            self.startChars = self.theFile.chars

        self.setText(self.theFile.text)

        return

    def loadFileVersion(self, filePath):

        self.theFile.setLoadFile(filePath)
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

    def autoSave(self):

        srcText = self.getText()

        self.theFile.setText(srcText)
        self.theFile.autoSaveText()

        self.textSaved = True
        self.fileSaved.set_from_file(self.ledGreen)

        return True

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):
        guiEditable = guiObject.get_active()
        self.set_editable(guiEditable)
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
        srcText = self.getText()
        srcText = htmlStrip(srcText)
        self.setText(srcText)
        return

    # Button Removed
    """"
    def onEditColour(self, guiObject):
        guiDialog = Gtk.ColorSelectionDialog("Select Colour")
        guiDialog.set_transient_for(self.guiParent)
        if guiDialog.run() == Gtk.ResponseType.OK:
            selCol = guiDialog.get_color_selection().get_current_color()
            colR   = int(floor(selCol.red   / 256))
            colG   = int(floor(selCol.green / 256))
            colB   = int(floor(selCol.blue  / 256))
            strCol = "#%02x%02x%02x" % (colR,colG,colB)
            self.execute_script("document.execCommand('forecolor', null, '%s');" % strCol)
        guiDialog.destroy()
        return
    """

    def onEventKeyPress(self, guiObject, guiEvent):
        #keyname = Gdk.keyval_name(guiEvent.keyval)
        #logger.debug("Editor key press: %s", keyname)
        return

    def onContentChanged(self, guiObject):
        logger.debug("Editor content changed")
        if self.textSaved:
            self.textSaved = False
            self.fileSaved.set_from_file(self.ledRed)
        return

    ##
    #  Getters
    ##

    """
    def getHtml(self):
        self.execute_script("document.title=document.documentElement.innerHTML;")
        #srcHtml = self.get_main_frame().get_data_source().get_data()
        #return srcHtml.str
        return unicode(self.get_main_frame().get_title(),"utf-8")
    """

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

        srcHtml  = "<html>"
        srcHtml += "<head>"
        srcHtml += "  <style>"
        srcHtml += "    body {font-size: "+fontSize+"px; padding: 40px;}"
        srcHtml += "    p    {margin: "+parMargin+"px; text-align: justify; line-height: "+lineHeight+"em;}"
        srcHtml += "    p+p  {text-indent: "+lineIndent+"em;}"
        srcHtml += "  </style>"
        srcHtml += "</head>"
        srcHtml += "<body>"+srcText+"</body>"
        srcHtml += "</html>"

        self.load_html_string(srcHtml,"file:///")

        return True

    def setEditable(self, editable):
        self.getObject("btnEditFile").set_active(editable)
        self.set_editable(editable)
        return

    """
    def setAsSaved(self):

        self.textSaved = True
        self.fileSaved.set_from_file(self.mainConf.guiPath+"/led-green.png")

        return
    """

# End Class Editor
