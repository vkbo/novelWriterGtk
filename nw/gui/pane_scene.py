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
from nw.file.doc         import DocFile

logger = logging.getLogger(__name__)

class GuiSceneEditor(Gtk.Paned):
    
    def __init__(self, theBook, itemHandle):
        
        Gtk.Paned.__init__(self)
        
        self.mainConf    = nw.CONFIG
        self.theBook     = theBook
        self.itemHandle  = itemHandle
        self.treeItem    = theBook.getTreeEntry(itemHandle)
        self.docLoaded   = False
        self.noteLoaded  = False
        self.docChanged  = False
        self.noteChanged = False
        
        # Pane Between Document and Details/Notes
        self.set_name("panedEditor")
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_position(self.mainConf.editPane)
        
        # Document Editor
        self.editDoc = GuiDocEditor()
        self.pack1(self.editDoc,True,False)
        
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
        self.editNote = GuiNoteEditor()
        self.panedMeta.pack2(self.editNote,True,False)
        
        # Signals
        self.editDoc.textBuffer.connect("changed",self.onDocChange)
        
        return
    
    def loadContent(self):
        
        docEntry = self.treeItem["entry"]
        docItem  = self.treeItem["doc"]
        docItem.openFile()
        
        self.editDoc.entryDocTitle.set_text(docEntry.itemName)
        self.editDoc.textBuffer.set_text("\n".join(docItem.docMain[0]["text"]))
        self.docLoaded = True
        
        return
    
    def saveContent(self):
        
        docEntry   = self.treeItem["entry"]
        docItem    = self.treeItem["doc"]
        
        textBuffer = self.editDoc.textBuffer
        parText, textCount = textBuffer.encodeText()
        
        docItem.setText(DocFile.DOC_MAIN,parText,textCount)
        docItem.saveFile()
        
        tabIcon = self.get_parent().get_tab_label(self).get_children()[0]
        tabIcon.set_from_icon_name("gtk-file",1)
        
        return
        
    def onDocChange(self, guiObject):
        
        if not self.docLoaded: return
        
        self.docChanged = True
        
        # print(guiObject)
        # print(self.get_parent())
        # print(self.get_parent().page_num(self))
        # print(self.get_parent().get_tab_label(self))
        # print(self.get_parent().get_tab_label(self).get_children()[0])
        tabIcon = self.get_parent().get_tab_label(self).get_children()[0]
        tabIcon.set_from_icon_name("gtk-about",1)
        
        
        return
    
# End Class GuiSceneEditor
