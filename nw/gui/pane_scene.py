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
        self.docItem  = None
        
        # Pane Between Document and Details/Notes
        self.set_name("panedEditor")
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_position(self.mainConf.editPane)
        
        # Document Editor
        self.scenePane = GuiDocEditor()
        self.pack1(self.scenePane,True,False)
        
        # Pane Between Details and Notes
        self.panedMeta = Gtk.Paned()
        self.panedMeta.set_name("panedMeta")
        self.panedMeta.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedMeta.set_position(self.mainConf.metaPane)
        self.pack2(self.panedMeta,True,False)
        
        # Document Details
        self.alignDocDetails = GuiDocDetails()
        self.panedMeta.pack1(self.alignDocDetails,True,False)
        
        # Document Notes
        self.notePane = GuiNoteEditor()
        self.panedMeta.pack2(self.notePane,True,False)
        
        return
    
    def loadContent(self, docItem):
        
        self.docItem = docItem
        self.docItem.openFile()
        
        self.scenePane.textBuffer.set_text(self.docItem.docText)
        
        return
    
    def saveContent(self):
        
        if self.docItem == None:
            logger.error("Nowhere to save content of scene editor")
            return
        
        textBuffer = self.scenePane.textBuffer
        bufFormat  = textBuffer.register_serialize_tagset()
        bufStart   = textBuffer.get_start_iter()
        bufEnd     = textBuffer.get_end_iter()
        bufSerial  = textBuffer.serialize(textBuffer,bufFormat,bufStart,bufEnd)
        
        self.docItem.setText(bufSerial)
    
# End Class GuiSceneEditor
