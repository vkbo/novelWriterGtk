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

from gi.repository       import Gtk, Gdk, Pango
from os                  import path
from nw.gui.edit_doc     import GuiDocEditor
from nw.gui.edit_note    import GuiNoteEditor
from nw.gui.pane_details import GuiDocDetails
from nw.file.book        import BookItem
from nw.file.doc         import DocFile

logger = logging.getLogger(__name__)

class GuiEditor(Gtk.Paned):
    
    def __init__(self, theBook, itemHandle):
        
        Gtk.Paned.__init__(self)
        
        self.mainConf    = nw.CONFIG
        self.theBook     = theBook
        
        self.itemHandle  = itemHandle
        self.treeItem    = theBook.getTreeEntry(itemHandle)
        self.itemClass   = self.treeItem["entry"].itemClass
        
        self.docLoaded   = False
        self.noteLoaded  = False
        self.docChanged  = False
        self.noteChanged = False
        
        # Pane Between Document and Details/Notes
        self.set_name("panedEditor")
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_position(self.mainConf.editPane)
        
        # Document Editor
        self.editDoc = GuiDocEditor(self.itemClass)
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
        if self.itemClass == BookItem.CLS_SCENE:
            self.editNote = GuiNoteEditor()
            self.panedMeta.pack2(self.editNote,True,False)
        else:
            self.editNote = None
        
        # Signals
        self.editDoc.textBuffer.connect("changed",self.onDocChange)
        self.editDoc.textView.connect("key-press-event",self.onKeyPress)
        
        return
    
    def loadContent(self):
        
        docEntry = self.treeItem["entry"]
        docItem  = self.treeItem["doc"]
        docItem.openFile()
        
        self.editDoc.entryDocTitle.set_text(docEntry.getFromTag(docEntry.TAG_NAME))
        
        self.editDoc.textBuffer.decodeText(docItem.docText[DocFile.VAL_TEXT])
        self.docLoaded = True
            
        if self.itemClass == BookItem.CLS_SCENE:
            self.editNote.textBuffer.decodeText(docItem.docText[DocFile.VAL_NOTE])
            self.noteLoaded = True
        
        return
    
    def saveContent(self):
        
        docEntry   = self.treeItem["entry"]
        docItem    = self.treeItem["doc"]
        
        textBuffer = self.editDoc.textBuffer
        parText, textCount = textBuffer.encodeText()
        
        docTitle = self.editDoc.entryDocTitle.get_text().strip()
        docEntry.setCounts(textCount)
        docEntry.setName(docTitle)
        
        if self.itemClass == BookItem.CLS_SCENE:
            noteBuffer = self.editNote.textBuffer
            parNote, noteCount = noteBuffer.encodeText()
        else:
            parNote = []
        
        docItem.setText(parText,textCount,parNote)
        docItem.saveFile()
        
        tabIcon = self.get_parent().get_tab_label(self).get_children()[0]
        tabIcon.set_from_icon_name("gtk-file",Gtk.IconSize.MENU)
        
        tabLabel = self.get_parent().get_tab_label(self).get_children()[1]
        tabLabel.set_text(docTitle)
        
        return
        
    def onKeyPress(self, guiObject, guiKeyEvent):
        
        # print(guiKeyEvent.state)
        # if guiKeyEvent.state == Gdk.ModifierType.CONTROL_MASK:
        #     print(guiKeyEvent.keyval)
        
        return
    
    def onDocChange(self, guiObject):
        
        if not self.docLoaded: return
        
        self.docChanged = True
        
        tabIcon = self.get_parent().get_tab_label(self).get_children()[0]
        tabIcon.set_from_icon_name("gtk-about",Gtk.IconSize.MENU)
        
        
        return
    
# End Class GuiSceneEditor
