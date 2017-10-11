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

from gi.repository import Gtk, Pango
from os            import path
from nw.content    import getLoremIpsum

logger = logging.getLogger(__name__)

class GuiDocEditor(Gtk.Alignment):

    def __init__(self):

        Gtk.Alignment.__init__(self)
        
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
        self.btnEditBold       = Gtk.ToolButton(icon_name="format-text-bold-symbolic")
        self.btnEditItalic     = Gtk.ToolButton(icon_name="format-text-italic-symbolic")
        self.btnEditUnderlince = Gtk.ToolButton(icon_name="format-text-underline-symbolic")
        self.btnAlignLeft      = Gtk.RadioToolButton()
        self.btnAlignCenter    = Gtk.RadioToolButton.new_from_widget(self.btnAlignLeft)
        self.btnAlignRight     = Gtk.RadioToolButton.new_from_widget(self.btnAlignCenter)
        self.btnAlignFill      = Gtk.RadioToolButton.new_from_widget(self.btnAlignRight)
        self.btnEditClear      = Gtk.ToolButton(icon_name="edit-clear-symbolic")
        self.btnAlignLeft.set_icon_name("format-justify-left-symbolic")
        self.btnAlignCenter.set_icon_name("format-justify-center-symbolic")
        self.btnAlignRight.set_icon_name("format-justify-right-symbolic")
        self.btnAlignFill.set_icon_name("format-justify-fill-symbolic")
        self.tbEdit.insert(self.btnEditBold,0)
        self.tbEdit.insert(self.btnEditItalic,1)
        self.tbEdit.insert(self.btnEditUnderlince,2)
        self.tbEdit.insert(Gtk.SeparatorToolItem(),3)
        self.tbEdit.insert(self.btnAlignLeft,4)
        self.tbEdit.insert(self.btnAlignCenter,5)
        self.tbEdit.insert(self.btnAlignRight,6)
        self.tbEdit.insert(self.btnAlignFill,7)
        self.tbEdit.insert(Gtk.SeparatorToolItem(),8)
        self.tbEdit.insert(self.btnEditClear,9)
        self.boxOuter.pack_start(self.tbEdit,False,True,0)

        self.scrollDoc = Gtk.ScrolledWindow()
        self.scrollDoc.set_hexpand(True)
        self.scrollDoc.set_vexpand(True)
        self.boxOuter.pack_start(self.scrollDoc,True,True,0)

        self.textView   = Gtk.TextView()
        self.textBuffer = self.textView.get_buffer()
        self.textBuffer.set_text("\n".join(getLoremIpsum(5)))
        self.textView.set_name("textViewDoc")
        self.scrollDoc.add(self.textView)

        self.tagBold      = self.textBuffer.create_tag("bold",weight=Pango.Weight.BOLD)
        self.tagItalic    = self.textBuffer.create_tag("italic",style=Pango.Style.ITALIC)
        self.tagUnderline = self.textBuffer.create_tag("underline",underline=Pango.Underline.SINGLE)
        
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textView.set_indent(30)
        self.textView.set_justification(Gtk.Justification.FILL)
        self.textView.set_pixels_below_lines(4)
        self.textView.modify_font(Pango.FontDescription("Tinos 15"))


        return

# End Class GuiDocEditor
