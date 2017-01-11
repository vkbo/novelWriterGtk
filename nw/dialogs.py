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

    def __init__(self):

        #Gtk.Dialog.__init__(self,"",BUILDER.get_object("winMain"),0,
        #    (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OK,Gtk.ResponseType.OK))
        Gtk.Dialog.__init__(self)

        self.mainConf   = CONFIG
        self = BUILDER.get_object("dlgEditBook")
        #self.set_transient_for(BUILDER.get_object("winMain"))

        self.show_all()
        self.hide()
        
        return

# End Class EditBookDialog
