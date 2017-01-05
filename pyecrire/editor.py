# -*- coding: utf-8 -*

##
#  pyÉcrire – Editor Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#  Manages the WebKit editor
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository      import Gtk, Gdk, WebKit
from os                 import getcwd
from math               import floor
from pyecrire.functions import htmlCleanUp

class Editor(WebKit.WebView):

    def __init__(self, builder, config):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        self.set_editable(False)
        self.connect("key_press_event",self.onEventKeyPress)
        self.load_html_string("", "file:///")

        return

    ##
    #  Events
    ##

    def onToggleEditable(self, guiObject):
        guiEditable = guiObject.get_active()
        self.set_editable(guiEditable)
        return

    def onEditAction(self, guiObject):
        logger.debug("Editor action %s" % guiObject.get_name())
        self.execute_script("document.execCommand('%s', false, false);" % guiObject.get_name())
        return

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

    def onEventKeyPress(self, guiObject, guiEvent):
        keyname = Gdk.keyval_name(guiEvent.keyval)
        #logger.debug("Editor key press: %s", keyname)
        return

    ##
    #  Getters
    ##

    def getHtml(self):
        self.execute_script("document.title=document.documentElement.innerHTML;")
        #srcHtml = self.get_main_frame().get_data_source().get_data()
        #return srcHtml.str
        return self.get_main_frame().get_title()

    def getText(self):

        self.execute_script("document.title=document.documentElement.innerHTML;")
        srcHtml = self.get_main_frame().get_title()

        bodyStart = srcHtml.find("<body")
        bodyStart = srcHtml.find(">",bodyStart)+1
        bodyEnd   = srcHtml.find("</body>")

        return htmlCleanUp(srcHtml[bodyStart:bodyEnd])

    ##
    #  Setters
    ##

    def setText(self, srcText):

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

        return

    def setEditable(self, editable):
        self.getObject("btnEditFile").set_active(editable)
        self.set_editable(editable)
        return

# End Class Editor
