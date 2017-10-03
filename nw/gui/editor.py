# -*- coding: utf-8 -*
"""novelWriter Web Editor Class

novelWriter – Web Editor Class
==============================
Main wrapper class for the GUI text editor

File History:
Created:   2017-01-10 [0.1.0]
Rewritten: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")
gi.require_version("WebKit","3.0")

from gi.repository import Gtk, WebKit
from os            import path

logger = logging.getLogger(__name__)

class GuiEditor(WebKit.WebView):

    def __init__(self):

        WebKit.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = nw.CONFIG

        # Paths
        self.htmlRoot   = "file://"+self.mainConf.guiPath.replace("\\","/")

        # Set Up Editor
        self.set_editable(False)
        self.load_html_string("",self.htmlRoot)

        setEditor = self.get_settings()
        setEditor.set_property("enable-default-context-menu",False)
        setEditor.set_property("spell-checking-languages",self.mainConf.spellCheck)
        self.set_settings(setEditor)

        return

# End Class GuiEditor
