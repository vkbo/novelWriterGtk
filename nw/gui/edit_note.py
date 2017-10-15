# -*- coding: utf-8 -*
"""novelWriter Note Editor Class

 novelWriter – Note Editor Class
=================================
 Main wrapper class for the GUI note editor

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

logger = logging.getLogger(__name__)

class GuiNoteEditor(Gtk.Alignment):
    
    def __init__(self):
        
        Gtk.Alignment.__init__(self)
        
        self.set_name("alignNoteEdit")
        self.set_padding(20,40,10,40)
        
        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxNoteOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing(0)
        self.add(self.boxOuter)
        
        self.lblTitle = Gtk.Label()
        self.lblTitle.set_name("lblNoteTitle")
        self.lblTitle.set_label("Notes")
        self.lblTitle.set_xalign(0.0)
        self.lblTitle.set_margin_bottom(12)
        self.boxOuter.pack_start(self.lblTitle,False,False,0)
        
        # Editor toolbar
        self.tbEdit = Gtk.Toolbar()
        self.tbEdit.set_name("tbNoteEdit")
        self.tbEdit.set_icon_size(Gtk.IconSize.MENU)
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
        # self.tbEdit.insert(Gtk.SeparatorToolItem(),4)
        # self.tbEdit.insert(self.btnAlignLeft,5)
        # self.tbEdit.insert(self.btnAlignCenter,6)
        # self.tbEdit.insert(self.btnAlignRight,7)
        # self.tbEdit.insert(self.btnAlignFill,8)
        # self.tbEdit.insert(Gtk.SeparatorToolItem(),9)
        # self.tbEdit.insert(self.btnEditClear,10)
        self.boxOuter.pack_start(self.tbEdit,False,True,0)
        
        self.scrollNote = Gtk.ScrolledWindow()
        self.scrollNote.set_name("scrollNote")
        self.scrollNote.set_hexpand(True)
        self.scrollNote.set_vexpand(True)
        self.boxOuter.pack_start(self.scrollNote,True,True,0)
        
        self.textView = GtkSource.View()
        self.textView.set_name("textViewNote")
        self.textView.set_margin_top(10)
        self.textView.set_margin_bottom(10)
        self.textView.set_margin_left(10)
        self.textView.set_margin_right(10)
        self.scrollNote.add(self.textView)
        
        self.textBuffer = NWTextBuffer()
        self.textBuffer.set_highlight_syntax(False)
        self.textBuffer.set_max_undo_levels(-1)
        self.textView.set_buffer(self.textBuffer)
        
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.set_indent(0)
        self.textView.set_justification(Gtk.Justification.LEFT)
        self.textView.set_pixels_below_lines(8)
        
        self.tagBold   = self.textBuffer.tagBold
        self.tagItalic = self.textBuffer.tagItalic
        self.tagMark   = self.textBuffer.tagMark
        self.tagStrike = self.textBuffer.tagStrike
        
        self.btnEditBold.connect("clicked",self.onButtonClick,self.tagBold)
        self.btnEditItalic.connect("clicked",self.onButtonClick,self.tagItalic)
        self.btnEditUnderline.connect("clicked",self.onButtonClick,self.tagMark)
        self.btnEditStrike.connect("clicked",self.onButtonClick,self.tagStrike)
        
        return
    
    def onButtonClick(self, guiObject, textTag):
        selBounds = self.textBuffer.get_selection_bounds()
        if len(selBounds) != 0:
            selStart, selEnd = selBounds
            self.textBuffer.apply_tag(textTag, selStart, selEnd)
        return
    
# End Class GuiNoteEditor
