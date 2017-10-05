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
gi.require_version("WebKit2","4.0")

from gi.repository import Gtk, Gdk, GLib, WebKit2
from os            import path
from nw.content    import getLoremIpsum, htmDemo

logger = logging.getLogger(__name__)

class GuiEditor(WebKit2.WebView):

    def __init__(self):

        WebKit2.WebView.__init__(self)

        # Connect to GUI
        self.mainConf   = nw.CONFIG

        # Paths
        self.htmlRoot   = "file://"+self.mainConf.themePath.replace("\\","/")
        self.set_name("webEditor")
        
        # GLib.threads_init()
        # Gdk.threads_init()

        # stateFlags = [
        #     Gtk.StateFlags.ACTIVE,
        #     Gtk.StateFlags.BACKDROP,
        #     Gtk.StateFlags.DIR_LTR,
        #     Gtk.StateFlags.DIR_RTL,
        #     Gtk.StateFlags.FOCUSED,
        #     Gtk.StateFlags.INCONSISTENT,
        #     Gtk.StateFlags.INSENSITIVE,
        #     Gtk.StateFlags.NORMAL,
        #     Gtk.StateFlags.PRELIGHT,
        #     Gtk.StateFlags.SELECTED
        # ]
        # self.set_background_color(Gdk.RGBA(0,0,0,0.5))

        # for stateFlag in stateFlags:
        #     self.override_background_color(stateFlag, Gdk.RGBA(0,0,0,0))
        
        tmpPars   = getLoremIpsum(13)
        tmpText   = ("".join(["<p>%s</p>"]*len(tmpPars))) % tuple(tmpPars)
        htmSimple = htmDemo(tmpText)

        # Set Up Editor
        self.set_editable(False)
        self.load_html(htmSimple,self.htmlRoot)

        # setEditor = self.get_settings()
        # setEditor.set_property("enable-default-context-menu",False)
        # setEditor.set_property("spell-checking-languages",self.mainConf.spellCheck)
        # self.set_settings(setEditor)

        return

# End Class GuiEditor
