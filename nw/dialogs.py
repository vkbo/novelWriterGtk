# -*- coding: utf-8 -*

##
#  novelWriter – Dialog Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Wrapper class for GUI dialogs.
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from os            import path
from gi.repository import Gtk
from nw            import *

class EditBookDialog(Gtk.Dialog):

    def __init__(self, nwAction):

        Gtk.Dialog.__init__(self,"",BUILDER.get_object("winMain"),0,
            ("Cancel",Gtk.ResponseType.CANCEL,"Save",Gtk.ResponseType.ACCEPT))

        self.mainConf = CONFIG

        # Title
        lblTitle = Gtk.Label("")
        lblTitle.set_markup("<span weight='medium' size='16896'>Book Options</span>")
        lblTitle.set_xalign(0.0)

        # Book Title
        fmeBookTitle = Gtk.Frame()
        fmeBookTitle.set_label("")
        fmeBookTitle.get_label_widget().set_markup("<span weight='bold' size='9011'>Title</span>")
        fmeBookTitle.set_shadow_type(Gtk.ShadowType.NONE)

        alignBookTitle = Gtk.Alignment()
        alignBookTitle.set_padding(2,2,12,4)
        alignBookTitle.set_size_request(400,-1)
        fmeBookTitle.add(alignBookTitle)
        self.entryBookTitle = Gtk.Entry()
        alignBookTitle.add(self.entryBookTitle)

        # Book Author
        fmeBookAuthor = Gtk.Frame()
        fmeBookAuthor.set_label("")
        fmeBookAuthor.get_label_widget().set_markup("<span weight='bold' size='9011'>Author</span>")
        fmeBookAuthor.set_shadow_type(Gtk.ShadowType.NONE)

        alignBookAuthor = Gtk.Alignment()
        alignBookAuthor.set_padding(2,2,12,4)
        alignBookAuthor.set_size_request(400,-1)
        fmeBookAuthor.add(alignBookAuthor)
        self.entryBookAuthor = Gtk.Entry()
        alignBookAuthor.add(self.entryBookAuthor)

        # Book Path
        fmeBookPath = Gtk.Frame()
        fmeBookPath.set_label("")
        fmeBookPath.get_label_widget().set_markup("<span weight='bold' size='9011'>Path</span>")
        fmeBookPath.set_shadow_type(Gtk.ShadowType.NONE)

        alignBookPath = Gtk.Alignment()
        alignBookPath.set_padding(2,2,12,4)
        alignBookPath.set_size_request(400,-1)
        fmeBookPath.add(alignBookPath)

        if nwAction == ACTION_NEW:
            self.fileBookPath = Gtk.FileChooserButton("Open Book Folder")
            self.fileBookPath.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
            alignBookPath.add(self.fileBookPath)

        if nwAction == ACTION_EDIT:
            self.entryBookPath = Gtk.Entry()
            self.entryBookPath.set_editable(False)
            alignBookPath.add(self.entryBookPath)

        # Add to Box
        guiBox = self.get_content_area()
        guiBox.set_margin_left(12)
        guiBox.set_margin_right(12)
        guiBox.set_margin_top(12)
        guiBox.set_margin_bottom(12)
        guiBox.set_spacing(5)

        guiBox.add(lblTitle)
        guiBox.add(Gtk.HSeparator())
        guiBox.add(fmeBookTitle)
        guiBox.add(fmeBookAuthor)
        guiBox.add(fmeBookPath)

        self.show_all()
        
        return

# End Class EditBookDialog
