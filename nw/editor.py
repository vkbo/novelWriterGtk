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

from gi.repository import Gtk, Gdk, WebKit
from nw            import *

class Editor(WebKit.WebView):

    def __init__(self, timer):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object
        self.guiTimer   = timer
        self.fileStatus = self.getObject("imgStatusFile")

        # Paths
        self.ledGrey    = self.mainConf.guiPath+"/led-grey.png"
        self.ledGreen   = self.mainConf.guiPath+"/led-green.png"
        self.ledRed     = self.mainConf.guiPath+"/led-red.png"

        # Set Up Editor
        self.set_editable(False)
        self.connect("user-changed-contents",self.onContentChanged)
        self.load_html_string("", "file:///")
        self.fileStatus.set_from_file(self.ledGrey)

        # Properties
        self.textSaved  = True

        return

    def clearEditor(self):

        if not self.textSaved: return False

        self.load_html_string("", "file:///")
        self.fileStatus.set_from_file(self.ledGrey)

        return True

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):
        self.setEditable(guiObject.get_active(),"Button")
        return

    def onEditAction(self, guiObject):
        logger.debug("Editor: Action %s" % guiObject.get_name())
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

    def onContentChanged(self, guiObject):

        if self.textSaved:
            self.textSaved = False
            self.fileStatus.set_from_file(self.ledRed)

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

        srcHtml  = "<html>"
        srcHtml += "<head>"
        srcHtml += "  <style>"
        srcHtml += "    body {font-size: "+fontSize+"px; padding: 40px; line-height: "+lineHeight+"em;}"
        srcHtml += "    p    {margin: "+parMargin+"px 0; text-align: justify;}"
        srcHtml += "    p+p  {text-indent: "+lineIndent+"em;}"
        srcHtml += "  </style>"
        srcHtml += "</head>"
        srcHtml += "<body>"+srcText+"</body>"
        srcHtml += "</html>"

        self.load_html_string(srcHtml,"file:///")

        return True

    def setEditable(self, makeEditable, fromButton=False):

        if fromButton:
            self.getObject("toggleFileEditable").set_active(makeEditable)
        self.set_editable(makeEditable)

        return

# End Class Editor
