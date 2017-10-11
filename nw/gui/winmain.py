# -*- coding: utf-8 -*
"""novelWriter GUI Main Window

novelWriter – GUI Main Window
=============================
Class holding the main window

File History:
Created: 2017-10-03 [0.4.0]

"""

import logging
import nw
import nw.const as NWC
import gi
gi.require_version("Gtk","3.0")

from gi.repository     import Gtk, Gdk, GLib
from nw.gui.bookpane   import GuiBookPane
from nw.gui.charspane  import GuiCharsPane
from nw.gui.plotspane  import GuiPlotsPane
from nw.gui.doceditor  import GuiDocEditor
from nw.gui.noteeditor import GuiNoteEditor
from nw.gui.docdetails import GuiDocDetails
from nw.gui.maintree   import GuiMainTree

logger = logging.getLogger(__name__)

class GuiWinMain(Gtk.ApplicationWindow):
    
    def __init__(self, theBook):
        Gtk.ApplicationWindow.__init__(self)
        logger.verbose("Starting building main window")
        
        self.mainConf = nw.CONFIG
        self.theBook  = theBook
        
        # theScreen = self.get_screen()
        # theVisual = theScreen.get_rgba_visual()
        # theVisual = theScreen.get_system_visual()
        
        # self.set_visual(theVisual)
        # self.set_app_paintable(True)
        self.set_title(self.mainConf.appName)
        self.resize(self.mainConf.winWidth,self.mainConf.winHeight)
        self.set_position(Gtk.WindowPosition.CENTER)
        # self.set_opacity(0.3)
        self.set_css_name("winMain")
        
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
        self.btnMainNew    = Gtk.ToolButton(icon_name="gtk-new")
        self.btnMainOpen   = Gtk.ToolButton(icon_name="gtk-open")
        self.btnMainSave   = Gtk.ToolButton(icon_name="gtk-save")
        self.btnMainSaveAs = Gtk.ToolButton(icon_name="gtk-save-as")
        self.tbMain.insert(self.btnMainNew,0)
        self.tbMain.insert(self.btnMainOpen,1)
        self.tbMain.insert(self.btnMainSave,2)
        self.tbMain.insert(self.btnMainSaveAs,3)
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
        
        # The Tree
        self.treeLeft = GuiMainTree(self.theBook)
        self.boxLeft.pack_start(self.treeLeft,True,True,0)
        
        # TreeView toolbar
        self.tbLeft = Gtk.Toolbar()
        self.tbLeft.set_name("tbLeft")
        self.tbLeft.set_icon_size(2)
        self.tbLeft.set_margin_top(4)
        self.tbLeft.set_margin_bottom(12)
        self.tbLeft.set_margin_left(12)
        self.tbLeft.set_margin_right(12)
        self.tbLeft.set_halign(Gtk.Align.END)
        self.btnLeftAdd = Gtk.ToolButton()
        self.btnLeftDel = Gtk.ToolButton()
        self.btnLeftAdd.set_label("Add")
        self.btnLeftDel.set_label("Remove")
        self.btnLeftAdd.set_homogeneous(False)
        self.btnLeftDel.set_homogeneous(False)
        self.tbLeft.insert(self.btnLeftAdd,0)
        self.tbLeft.insert(self.btnLeftDel,1)
        self.boxLeft.pack_start(self.tbLeft,False,True,0)
        
        #
        # Main Content
        #
        
        # Notebook Holding the Main Content
        self.nbContent = Gtk.Notebook()
        self.nbContent.set_name("nbContent")
        self.nbContent.set_show_tabs(False)
        self.nbContent.set_show_border(False)
        self.nbContent.set_tab_pos(Gtk.PositionType.RIGHT)
        self.panedOuter.pack2(self.nbContent,True,False)
        
        #
        # Notebook: Book Page
        #
        
        # Outer Scroll Window
        self.scrollBook = Gtk.ScrolledWindow()
        self.scrollBook.set_name("scrollBook")
        self.nbContent.insert_page(self.scrollBook,None,NWC.NBTabs.BOOK.value)
        
        # Book Alignment
        self.alignBook = GuiBookPane(self.theBook)
        self.scrollBook.add(self.alignBook)
        
        #
        # Notebook: Characters Page
        #
        
        # Outer Scroll Window
        self.scrollChars = Gtk.ScrolledWindow()
        self.scrollChars.set_name("scrollChars")
        self.nbContent.insert_page(self.scrollChars,None,NWC.NBTabs.CHARS.value)
        
        # Book Alignment
        self.alignChars = GuiCharsPane(self.theBook)
        self.scrollChars.add(self.alignChars)
        
        #
        # Notebook: Plots Page
        #
        
        # Outer Scroll Window
        self.scrollPlots = Gtk.ScrolledWindow()
        self.scrollPlots.set_name("scrollPlots")
        self.nbContent.insert_page(self.scrollPlots,None,NWC.NBTabs.PLOTS.value)
        
        # Book Alignment
        self.alignPlots = GuiPlotsPane(self.theBook)
        self.scrollPlots.add(self.alignPlots)

        #
        # Notebook: Editor Tab
        #
        
        # Pane Between Editor and Timeline
        self.panedContent = Gtk.Paned()
        self.panedContent.set_name("panedContent")
        self.panedContent.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedContent.set_position(self.mainConf.contPane)
        self.nbContent.insert_page(self.panedContent,None,NWC.NBTabs.EDITOR.value)
        
        # Pane Between Document and Details/Notes
        self.panedEditor = Gtk.Paned()
        self.panedEditor.set_name("panedEditor")
        self.panedEditor.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.panedEditor.set_position(self.mainConf.editPane)
        self.panedContent.pack1(self.panedEditor,True,False)
        
        # Document Editor
        self.alignDocEdit = GuiDocEditor()
        self.panedEditor.pack1(self.alignDocEdit,True,False)
        
        # Pane Between Details and Notes
        self.panedMeta = Gtk.Paned()
        self.panedMeta.set_name("panedMeta")
        self.panedMeta.set_orientation(Gtk.Orientation.VERTICAL)
        self.panedMeta.set_position(self.mainConf.metaPane)
        self.panedEditor.pack2(self.panedMeta,True,False)
        
        # Document Details
        self.alignDocDetails = GuiDocDetails()
        self.panedMeta.pack1(self.alignDocDetails,True,False)
        
        # Document Notes
        self.alignNoteEdit = GuiNoteEditor()
        self.panedMeta.pack2(self.alignNoteEdit,True,False)
        
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
        self.nbContent.set_current_page(tabNum.value)
        return

# End Class GUIwinMain
