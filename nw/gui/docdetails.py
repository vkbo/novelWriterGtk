# -*- coding: utf-8 -*
"""novelWriter Doc Details Class

 novelWriter – Doc Details Class
=================================
 Main wrapper class for the GUI doc details

 File History:
 Created:   2017-10-06 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, Pango
from os            import path

logger = logging.getLogger(__name__)

class GuiDocDetails(Gtk.Alignment):

    def __init__(self):

        Gtk.Alignment.__init__(self)
        
        self.set_name("alignDetailsEdit")
        self.set_padding(40,20,10,40)

        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxDetailsOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing(0)
        self.add(self.boxOuter)

        self.lblTitle = Gtk.Label()
        self.lblTitle.set_name("lblDetailsTitle")
        self.lblTitle.set_label("Details")
        self.lblTitle.set_xalign(0.0)
        self.lblTitle.set_margin_bottom(12)
        self.boxOuter.pack_start(self.lblTitle,False,False,0)


        return

# End Class GuiDocDetails
