# -*- coding: utf-8 -*
"""novelWriter Scene Editor Class

 novelWriter – Scene Editor Class
==================================
 Main wrapper class for the scene editor pane

 File History:
 Created:   2017-10-12 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository       import Gtk, Pango
from os                  import path
from nw.gui.edit_doc     import GuiDocEditor
from nw.gui.edit_note    import GuiNoteEditor
from nw.gui.pane_details import GuiDocDetails

logger = logging.getLogger(__name__)

class GuiSceneEditor(Gtk.Paned):
    
    def __init__(self, theBook):
        
        Gtk.Paned.__init__(self)
        
        self.mainConf = nw.CONFIG
        self.theBook  = theBook
        
        self.set_name("panedContent")
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_position(self.mainConf.contPane)
        
        # Pane Between Document and Details/Notes
        self.panedEditor = Gtk.Paned()
        self.panedEditor.set_name("panedEditor")
        self.panedEditor.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.panedEditor.set_position(self.mainConf.editPane)
        self.pack1(self.panedEditor,True,False)
        
        # Document Editor
        self.alignDocEdit = GuiDocEditor()
        self.panedEditor.pack1(self.alignDocEdit,True,False)
        
        # Pane Between Details and Notes
        self.panedMeta = Gtk.Paned()
        self.panedMeta.set_name("panedMeta")
        self.panedMeta.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedMeta.set_position(self.mainConf.metaPane)
        self.panedEditor.pack2(self.panedMeta,True,False)
        
        # Document Details
        self.alignDocDetails = GuiDocDetails()
        self.panedMeta.pack1(self.alignDocDetails,True,False)
        
        # Document Notes
        self.alignNoteEdit = GuiNoteEditor()
        self.panedMeta.pack2(self.alignNoteEdit,True,False)
        
        # Timeline
        self.scrlTimeLine = Gtk.ScrolledWindow()
        self.scrlTimeLine.set_name("scrlTimeLine")
        self.pack2(self.scrlTimeLine,True,False)
        
        self.drawTimeLine = Gtk.DrawingArea()
        self.drawTimeLine.set_name("drawTimeLine")
        self.scrlTimeLine.add(self.drawTimeLine)
        # self.drawTimeLine.connect("draw", self.onExpose)
        
        return
    
# End Class GuiSceneEditor
