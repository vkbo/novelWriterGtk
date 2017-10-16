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
gi.require_version("GtkSource","3.0")

from gi.repository     import Gtk, Pango
from gi.repository     import GtkSource
from os                import path
from nw.gui.textbuffer import NWTextBuffer
from nw.file           import BookItem

logger = logging.getLogger(__name__)

class GuiDocEditor(Gtk.Alignment):
    
    def __init__(self, itemClass):
        
        Gtk.Alignment.__init__(self)
        
        self.itemClass = itemClass
        
        self.set_name("alignDocEdit")
        self.set_padding(40,40,40,10)
        
        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxDocOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing(0)
        self.add(self.boxOuter)
        
        # Document Title
        self.fmeDocTitle = Gtk.Frame()
        self.fmeDocTitle.set_name("fmeDocTitle")
        self.fmeDocTitle.set_shadow_type(Gtk.ShadowType.NONE)
        self.boxOuter.pack_start(self.fmeDocTitle,False,False,0)
        
        self.alignDocTitle = Gtk.Alignment()
        self.alignDocTitle.set_padding(0,12,0,0)
        self.fmeDocTitle.add(self.alignDocTitle)
        
        self.entryDocTitle = Gtk.Entry()
        self.entryDocTitle.set_name("entryDocTitle")
        self.entryDocTitle.set_text("Document Title")
        self.alignDocTitle.add(self.entryDocTitle)
        
        # Editor toolbar
        self.tbEdit = Gtk.Toolbar()
        self.tbEdit.set_name("tbDocEdit")
        self.btnEditBold      = Gtk.ToolButton(icon_name="format-text-bold-symbolic")
        self.btnEditItalic    = Gtk.ToolButton(icon_name="format-text-italic-symbolic")
        self.btnEditUnderline = Gtk.ToolButton(icon_name="format-text-underline-symbolic")
        self.btnEditStrike    = Gtk.ToolButton(icon_name="format-text-strikethrough-symbolic")
        self.btnAlignLeft     = Gtk.RadioToolButton()
        self.btnAlignCenter   = Gtk.RadioToolButton.new_from_widget(self.btnAlignLeft)
        self.btnAlignRight    = Gtk.RadioToolButton.new_from_widget(self.btnAlignCenter)
        self.btnAlignFill     = Gtk.RadioToolButton.new_from_widget(self.btnAlignRight)
        self.btnEditClear     = Gtk.ToolButton(icon_name="edit-clear-symbolic")
        self.btnAlignLeft.set_icon_name("format-justify-left-symbolic")
        self.btnAlignCenter.set_icon_name("format-justify-center-symbolic")
        self.btnAlignRight.set_icon_name("format-justify-right-symbolic")
        self.btnAlignFill.set_icon_name("format-justify-fill-symbolic")
        self.tbEdit.insert(self.btnEditBold,0)
        self.tbEdit.insert(self.btnEditItalic,1)
        self.tbEdit.insert(self.btnEditUnderline,2)
        self.tbEdit.insert(self.btnEditStrike,3)
        self.tbEdit.insert(Gtk.SeparatorToolItem(),4)
        self.tbEdit.insert(self.btnAlignLeft,5)
        self.tbEdit.insert(self.btnAlignCenter,6)
        self.tbEdit.insert(self.btnAlignRight,7)
        self.tbEdit.insert(self.btnAlignFill,8)
        self.tbEdit.insert(Gtk.SeparatorToolItem(),9)
        self.tbEdit.insert(self.btnEditClear,10)
        self.boxOuter.pack_start(self.tbEdit,False,True,0)
        
        self.scrollDoc = Gtk.ScrolledWindow()
        self.scrollDoc.set_name("scrollDoc")
        self.scrollDoc.set_hexpand(True)
        self.scrollDoc.set_vexpand(True)
        self.boxOuter.pack_start(self.scrollDoc,True,True,0)
        
        self.textView   = GtkSource.View()
        self.textView.set_name("textViewDoc")
        self.textView.set_margin_top(20)
        self.textView.set_margin_bottom(20)
        self.textView.set_margin_left(20)
        self.textView.set_margin_right(20)
        self.scrollDoc.add(self.textView)
        
        self.textBuffer = NWTextBuffer()
        self.textBuffer.set_highlight_syntax(False)
        self.textBuffer.set_max_undo_levels(-1)
        self.textView.set_buffer(self.textBuffer)
        
        self.tagBold   = self.textBuffer.tagBold
        self.tagItalic = self.textBuffer.tagItalic
        self.tagMark   = self.textBuffer.tagMark
        self.tagStrike = self.textBuffer.tagStrike
        
        self.btnEditBold.connect("clicked",self.onToggleStyle,self.tagBold)
        self.btnEditItalic.connect("clicked",self.onToggleStyle,self.tagItalic)
        self.btnEditUnderline.connect("clicked",self.onToggleStyle,self.tagMark)
        self.btnEditStrike.connect("clicked",self.onToggleStyle,self.tagStrike)
        self.btnEditClear.connect("clicked",self.onClearStyle)
        
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.modify_font(Pango.FontDescription("Tinos 15"))
        if self.itemClass == BookItem.CLS_SCENE:
            self.textView.set_indent(30)
            self.textView.set_justification(Gtk.Justification.FILL)
            self.textView.set_pixels_below_lines(4)
        else:
            self.textView.set_indent(0)
            self.textView.set_justification(Gtk.Justification.LEFT)
            self.textView.set_pixels_below_lines(12)
        
        return
    
    def onToggleStyle(self, guiObject, textTag):
        self.textBuffer.toggleStyle(textTag)
        return
    
    def onClearStyle(self, guiObject):
        selBounds = self.textBuffer.get_selection_bounds()
        if len(selBounds) != 0:
            selStart, selEnd = selBounds
            self.textBuffer.remove_all_tags(selStart,selEnd)
        return
    
# End Class GuiDocEditor
