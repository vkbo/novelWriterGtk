# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit
from pyecrire.editor import Editor

import os

#class GUI(Gtk.Window):
class GUI():

    def __init__(self):

        self.guiBuilder = Gtk.Builder()
        self.guiBuilder.add_from_file("pyecrire/winMain.glade")
        self.getObject = self.guiBuilder.get_object
        self.winMain   = self.getObject("winMain")
        self.webEditor = Editor(self.winMain)

        guiHandlers = {
            "onDestroyWindow"          : self.guiDestroy,
            "onClickEditBold"          : self.webEditor.onEditAction,
            "onClickEditItalic"        : self.webEditor.onEditAction,
            "onClickEditUnderline"     : self.webEditor.onEditAction,
            "onClickEditStrikeThrough" : self.webEditor.onEditAction,
            "onClickEditColour"        : self.webEditor.onEditColour,
            "onSwitchPageMainNoteBook" : self.tabChange,
        }
        self.guiBuilder.connect_signals(guiHandlers)

        self.scrollEditor = self.guiBuilder.get_object("scrollEditor")
        self.scrollEditor.add(self.webEditor)

        self.winMain.resize(1000,700)
        self.winMain.show_all()

    def guiDestroy(self, guiObject):
        print("Exiting")
        Gtk.main_quit()

    def tabChange(self, guiObject, guiChild, tabIdx):
        print("Tab Change")
        if tabIdx == 2:
            print("Source View")
            strSource = self.webEditor.getHtml()
            bufferSource = Gtk.TextBuffer()
            bufferSource.set_text(strSource)
            textSource = self.getObject("textSource")
            textSource.set_buffer(bufferSource)
            print(strSource)


