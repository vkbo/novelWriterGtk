# -*- coding: utf-8 -*

##
#  pyÉcrire – Dialog Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#  Wrapper class for simple GUI dialogs.
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from pyecrire      import *

class OkCancelDialog(Gtk.Dialog):

    def __init__(self, dlgMessage):

        self.confMain  = CONFIG
        self.getObject = BUILDER.get_object
        self.guiParent = self.getObject("winMain")

        Gtk.Dialog.__init__(self,self.confMain.appName+" Dialog",self.guiParent,0,
            (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OK,Gtk.ResponseType.OK))

        guiLabel = Gtk.Label(dlgMessage)
        guiLabel.set_padding(8,12)

        guiBox   = self.get_content_area()
        guiBox.add(guiLabel)

        self.show_all()

# End Class OkCancelDialog
