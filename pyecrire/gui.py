# -*- coding: utf-8 -*

import gtk
import webkit
import os

class GUI(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("pyÉcrire")
        self.connect("destroy", gtk.main_quit)
        self.resize(1200, 800)

        self.guiEditor = webkit.WebView()
        self.guiEditor.set_editable(True)
        self.guiEditor.load_html_string("Hello Kitty", "file:///")

        self.guiScroll = gtk.ScrolledWindow()
        self.guiScroll.add(self.guiEditor)
        self.guiScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.guiTreeData = gtk.TreeStore(str)
        self.guiTreeView = gtk.TreeView(model=self.guiTreeData)

        self.guiVBox = gtk.VBox()
        self.guiHBox = gtk.HBox()
        self.guiHBox.pack_start(self.guiTreeView, True, True)
        self.guiHBox.pack_start(self.guiScroll, True, True)
        self.guiVBox.pack_start(self.guiHBox, True, True)
        self.add(self.guiVBox)
