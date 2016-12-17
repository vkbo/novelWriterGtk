# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit

import os

class Editor(WebKit.WebView):

    def __init__(self):
        WebKit.WebView.__init__(self)
        self.set_editable(True)
        self.load_html_string("<p>Hello Kitty</p>", "file:///")

    def onEditAction(self, guiObject):
        print("Action: %s" % guiObject.get_name())
        self.execute_script("document.execCommand('%s', false, false);" % guiObject.get_name())

