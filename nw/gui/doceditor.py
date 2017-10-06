# -*- coding: utf-8 -*
"""novelWriter Document Editor Class

 novelWriter – Document Editor Class
=====================================
 Main wrapper class for the GUI text editor

 File History:
 Created:   2017-10-06 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from nw.content    import getLoremIpsum, htmDemo

logger = logging.getLogger(__name__)

class GuiDocEditor(Gtk.Alignment):

    def __init__(self):

        Gtk.Alignment.__init__(self)
        
        self.set_name("alignDocEdit")
        self.set_padding(40,40,40,10)

        self.boxDocEdit = Gtk.Box()
        self.boxDocEdit.set_name("boxDocEdit")
        self.boxDocEdit.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxDocEdit.set_spacing(0)
        self.add(self.boxDocEdit)

        self.lblDocTitle = Gtk.Label()
        self.lblDocTitle.set_name("lblDocTitle")
        self.lblDocTitle.set_label("Document Title")
        self.lblDocTitle.set_xalign(0.0)
        self.boxDocEdit.pack_start(self.lblDocTitle,False,False,0)

        return

# End Class GuiDocEditor
