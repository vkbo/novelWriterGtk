# -*- coding: utf-8 -*

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit
from math import floor

import os

class Editor(WebKit.WebView):

    def __init__(self,guiParent):
        WebKit.WebView.__init__(self)
        self.guiParent = guiParent
        self.set_editable(True)
        self.load_html_string("<p>Hello Kitty</p>", "file:///")

    def onEditAction(self, guiObject):
        logger.debug("Editor action %s" % guiObject.get_name())
        self.execute_script("document.execCommand('%s', false, false);" % guiObject.get_name())

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

    def getHtml(self):
        self.execute_script("document.title=document.documentElement.innerHTML;")
        #srcHtml = self.get_main_frame().get_data_source().get_data()
        #return srcHtml.str
        return self.get_main_frame().get_title()


