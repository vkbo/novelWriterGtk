# -*- coding: utf-8 -*
"""novelWriter GUI Main Window

 novelWriter – GUI Main Window
===============================
 Class holding the main window

 File History:
 Created: 2017-10-03 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository      import Gtk, Gdk, GLib
from nw.gui.tree_main   import GuiMainTree
from nw.gui.pane_book   import GuiBookPane
from nw.gui.pane_chars  import GuiCharsPane
from nw.gui.pane_plots  import GuiPlotsPane
from nw.gui.pane_editor import GuiEditor

logger = logging.getLogger(__name__)

class GuiWinMain(Gtk.ApplicationWindow):
    
    TAB_BOOK = 0
    TAB_CHAR = 1
    TAB_PLOT = 2
    TAB_VIEW = 3
    TAB_EDIT = 4
    
    def __init__(self, theBook):
        Gtk.ApplicationWindow.__init__(self)
        logger.verbose("Starting building main window")
        
        self.mainConf  = nw.CONFIG
        self.theBook   = theBook
        self.editPages = {}
        
        self.set_title(self.mainConf.appName)
        self.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.set_name("winMain")
        
        #
        # Main Layout Items
        #
        
        # Outer Vertical Box
        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing = 0
        self.add(self.boxOuter)
        
        # Top Horisontal Box (TopBar)
        self.boxTop = Gtk.Box()
        self.boxTop.set_name("boxTop")
        self.boxTop.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.boxTop.set_spacing(0)
        self.boxOuter.pack_start(self.boxTop,False,False,0)
        
        # Main ToolBar
        self.tbMain = Gtk.Toolbar()
        self.tbMain.set_name("tbMain")
        self.tbMain.set_margin_top(8)
        self.tbMain.set_margin_bottom(8)
        self.tbMain.set_margin_left(12)
        self.tbMain.set_margin_right(12)
        self.btnMainNew       = Gtk.ToolButton(icon_name="accessories-dictionary-symbolic")
        self.btnMainOpen      = Gtk.ToolButton(icon_name="document-open-symbolic")
        self.btnMainSave      = Gtk.ToolButton(icon_name="document-save-symbolic")
        self.btnMainSaveAs    = Gtk.ToolButton(icon_name="document-save-as-symbolic")
        self.btnMainProjPrefs = Gtk.ToolButton(icon_name="document-properties-symbolic")
        self.btnMainProgPrefs = Gtk.ToolButton(icon_name="preferences-system-symbolic")
        self.btnMainNew.set_tooltip_text("New Book Project")
        self.btnMainOpen.set_tooltip_text("Open Book Project")
        self.btnMainSave.set_tooltip_text("Save Book Project")
        self.btnMainSaveAs.set_tooltip_text("Save Book Project As")
        self.btnMainProjPrefs.set_tooltip_text("Project Preferences")
        self.btnMainProgPrefs.set_tooltip_text("novelWriter Preferences")
        self.tbMain.insert(self.btnMainNew,0)
        self.tbMain.insert(self.btnMainOpen,1)
        self.tbMain.insert(self.btnMainSave,2)
        self.tbMain.insert(self.btnMainSaveAs,3)
        self.tbMain.insert(Gtk.SeparatorToolItem(),4)
        self.tbMain.insert(self.btnMainProjPrefs,5)
        self.tbMain.insert(self.btnMainProgPrefs,6)
        self.boxTop.pack_start(self.tbMain,False,True,0)
        
        # Pane for TreeView and Main Content
        self.panedOuter = Gtk.Paned()
        self.panedOuter.set_name("panedOuter")
        self.panedOuter.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.panedOuter.set_position(self.mainConf.mainPane)
        self.panedOuter.set_wide_handle(False)
        self.boxOuter.pack_start(self.panedOuter,True,True,0)
        
        #
        # Left Side Tree
        #
        
        # TreeView Vertical Box
        self.boxLeft = Gtk.Box()
        self.boxLeft.set_name("boxLeft")
        self.boxLeft.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxLeft.set_spacing(0)
        self.panedOuter.pack1(self.boxLeft,True,False)
        
        # TreeView Title
        self.lblLeft = Gtk.Label()
        self.lblLeft.set_name("lblLeft")
        self.lblLeft.set_label("Content")
        self.lblLeft.set_xalign(0.0)
        self.lblLeft.set_yalign(0.0)
        self.lblLeft.set_margin_top(4)
        self.lblLeft.set_margin_bottom(4)
        self.lblLeft.set_margin_left(12)
        self.lblLeft.set_margin_right(12)
        self.boxLeft.pack_start(self.lblLeft,False,False,0)
        
        # TreeView Toolbar
        self.tbLeft = Gtk.Toolbar()
        self.tbLeft.set_name("tbLeft")
        self.tbLeft.set_icon_size(Gtk.IconSize.MENU)
        self.tbLeft.set_margin_top(0)
        self.tbLeft.set_margin_bottom(4)
        self.tbLeft.set_margin_left(12)
        self.tbLeft.set_margin_right(12)
        self.tbLeft.set_halign(Gtk.Align.START)
        self.btnLeftAdd = Gtk.ToolButton(icon_name="list-add-symbolic")
        self.btnLeftDel = Gtk.ToolButton(icon_name="list-remove-symbolic")
        self.btnLeftMvU = Gtk.ToolButton(icon_name="go-up-symbolic")
        self.btnLeftMvD = Gtk.ToolButton(icon_name="go-down-symbolic")
        self.btnLeftNdU = Gtk.ToolButton(icon_name="go-top-symbolic")
        self.btnLeftNdD = Gtk.ToolButton(icon_name="go-bottom-symbolic")
        self.btnLeftAdd.set_tooltip_text("Add New File")
        self.btnLeftDel.set_tooltip_text("Remove Selected File")
        self.btnLeftMvU.set_tooltip_text("Move Item Up")
        self.btnLeftMvD.set_tooltip_text("Move Item Down")
        self.btnLeftNdU.set_tooltip_text("Move Item Up a Node")
        self.btnLeftNdD.set_tooltip_text("Move Item Down a Node")
        self.btnLeftAdd.set_homogeneous(True)
        self.btnLeftDel.set_homogeneous(True)
        self.btnLeftMvU.set_homogeneous(True)
        self.btnLeftMvD.set_homogeneous(True)
        self.btnLeftNdU.set_homogeneous(True)
        self.btnLeftNdD.set_homogeneous(True)
        self.tbLeft.insert(self.btnLeftAdd,0)
        self.tbLeft.insert(self.btnLeftDel,1)
        self.tbLeft.insert(self.btnLeftMvU,2)
        self.tbLeft.insert(self.btnLeftMvD,3)
        self.tbLeft.insert(self.btnLeftNdU,4)
        self.tbLeft.insert(self.btnLeftNdD,5)
        self.boxLeft.pack_start(self.tbLeft,False,True,0)
        
        # The Tree
        self.scrollLeft = Gtk.ScrolledWindow()
        self.scrollLeft.set_name("scrollLeft")
        self.scrollLeft.set_hexpand(True)
        self.scrollLeft.set_vexpand(True)
        self.boxLeft.pack_start(self.scrollLeft,True,True,0)
        
        self.treeLeft = GuiMainTree(self.theBook)
        self.scrollLeft.add(self.treeLeft)
        
        #
        # Main Content
        #
        
        self.panedContent = Gtk.Paned()
        self.panedContent.set_name("panedContent")
        self.panedContent.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedContent.set_position(self.mainConf.contPane)
        self.panedOuter.pack2(self.panedContent,True,False)
        
        # Notebook Holding the Main Content
        self.nbContent = Gtk.Notebook()
        self.nbContent.set_name("nbContent")
        self.nbContent.set_show_tabs(True)
        self.nbContent.set_show_border(False)
        self.nbContent.set_tab_pos(Gtk.PositionType.TOP)
        self.nbContent.set_scrollable(True)
        self.panedContent.pack1(self.nbContent,True,False)
        
        #
        # Notebook: Book Page
        #
        
        # Outer Scroll Window
        self.scrollBook = Gtk.ScrolledWindow()
        self.scrollBook.set_name("scrollBook")
        self.nbContent.insert_page(self.scrollBook,Gtk.Label("Book"),self.TAB_BOOK)
        
        # Book Alignment
        self.bookPage = GuiBookPane(self.theBook)
        self.scrollBook.add(self.bookPage)
        
        #
        # Notebook: Characters Page
        #
        
        # Outer Scroll Window
        self.scrollChars = Gtk.ScrolledWindow()
        self.scrollChars.set_name("scrollChars")
        self.nbContent.insert_page(self.scrollChars,Gtk.Label("Characters"),self.TAB_CHAR)
        
        # Book Alignment
        self.charPage = GuiCharsPane(self.theBook)
        self.scrollChars.add(self.charPage)
        
        #
        # Notebook: Plots Page
        #
        
        # Outer Scroll Window
        self.scrollPlots = Gtk.ScrolledWindow()
        self.scrollPlots.set_name("scrollPlots")
        self.nbContent.insert_page(self.scrollPlots,Gtk.Label("Plots"),self.TAB_PLOT)
        
        # Book Alignment
        self.plotPage = GuiPlotsPane(self.theBook)
        self.scrollPlots.add(self.plotPage)
        
        #
        # Notebook: View Page
        #
        
        self.scrollView = Gtk.ScrolledWindow()
        self.scrollView.set_name("scrollView")
        self.nbContent.insert_page(self.scrollView,Gtk.Label("View"),self.TAB_VIEW)
        
        #
        #  Timeline
        #
        
        # Timeline
        self.scrlTimeLine = Gtk.ScrolledWindow()
        self.scrlTimeLine.set_name("scrlTimeLine")
        self.panedContent.pack2(self.scrlTimeLine,True,False)
        
        self.drawTimeLine = Gtk.DrawingArea()
        self.drawTimeLine.set_name("drawTimeLine")
        self.scrlTimeLine.add(self.drawTimeLine)
        # self.drawTimeLine.connect("draw", self.onExpose)
        
        logger.verbose("Finished building main window")
        self.show_all()
        
        return
    
    def showTab(self, tabNum):
        logger.vverbose("WinMain: Switching tab to %s" % tabNum)
        self.nbContent.set_current_page(tabNum)
        return
    
    def viewFile(self, itemHandle):
        """Switches to the tab of a file if it's already open, but does not open
        a tab if it's not."""
        
        if itemHandle in self.editPages.keys():
            logger.verbose("Showing file with handle %s" % itemHandle)
            tabNum = self.editPages[itemHandle]["index"]
            self.nbContent.set_current_page(tabNum)
            return
        
        return
    
    def editFile(self, itemHandle):
        """Opens an edit window for a file"""
        
        logger.verbose("Editing file with handle %s" % itemHandle)
        
        if itemHandle in self.editPages.keys():
            tabNum = self.editPages[itemHandle]["index"]
            self.nbContent.set_current_page(tabNum)
            return
        
        logger.vverbose("Opening a new tab")
        
        treeEntry = self.theBook.getItem(itemHandle)
        
        tabBox = Gtk.Box()
        tabBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabBox.set_spacing(2)
        tabLabel = Gtk.Label(treeEntry["entry"].itemName)
        tabIcon = Gtk.Image()
        tabIcon.set_from_icon_name("emblem-default-symbolic",Gtk.IconSize.MENU)
        tabImage = Gtk.Image()
        tabImage.set_from_icon_name("window-close-symbolic",Gtk.IconSize.MENU)
        tabButton = Gtk.Button()
        tabButton.set_image(tabImage)
        tabButton.set_relief(Gtk.ReliefStyle.NONE)
        tabBox.pack_start(tabIcon,False,False,0)
        tabBox.pack_start(tabLabel,False,False,0)
        tabBox.pack_start(tabButton,False,False,0)
        
        newPage = GuiEditor(self.theBook,itemHandle)
        pageID  = self.nbContent.append_page(newPage,tabBox)
        self.nbContent.set_tab_reorderable(newPage,True)
        tabBox.show_all()
        newPage.show_all()
        newPage.loadContent()
        
        self.editPages[itemHandle] = {
            "index" : pageID,
            "item"  : newPage,
        }
        
        tabButton.connect("clicked",self.onCloseTab,itemHandle)
        self.nbContent.connect("page-reordered",self.onReorderTab)
        self.nbContent.set_current_page(pageID)
        
        return
    
    def onCloseTab(self, guiObject, itemHandle):
        
        pageID = self.nbContent.page_num(self.editPages[itemHandle]["item"])
        
        self.nbContent.remove_page(pageID)
        del self.editPages[itemHandle]
        
        return
    
    def onReorderTab(self, guiObject, guiChild, newPage):
        
        if newPage < self.TAB_EDIT:
            self.nbContent.reorder_child(guiChild,self.TAB_EDIT)
        
        return
    
# End Class GuiWinMain
