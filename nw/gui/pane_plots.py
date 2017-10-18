# -*- coding: utf-8 -*
"""novelWriter GUI Plots Pane

 novelWriter – GUI Plots Pane
==============================
 Main wrapper class for the GUI plots editor

 File History:
 Created: 2017-10-09 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository     import Gtk, Pango
from os                import path
from nw.gui.tree_plots import GuiPlotsTree

logger = logging.getLogger(__name__)

class GuiPlotsPane(Gtk.Alignment):
    
    def __init__(self, theBook):
        
        Gtk.Alignment.__init__(self)
        
        self.theBook = theBook
        
        # Book Alignment
        self.set_name("alignBook")
        self.set_padding(40,40,40,40)
        
        # Main Vertical Box
        self.boxPlots = Gtk.Box()
        self.boxPlots.set_name("boxPlots")
        self.boxPlots.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxPlots.set_spacing(8)
        self.add(self.boxPlots)
        
        # Top Horisontal Box
        self.boxTop = Gtk.Box()
        self.boxTop.set_name("boxPlotsTop")
        self.boxTop.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.boxTop.set_spacing(100)
        self.boxPlots.pack_start(self.boxTop,False,False,0)
        
        # Top Title
        self.lblPlots = Gtk.Label()
        self.lblPlots.set_name("lblPlots")
        self.lblPlots.set_label("Plots")
        self.lblPlots.set_xalign(0.0)
        self.lblPlots.set_yalign(0.0)
        self.boxTop.pack_start(self.lblPlots,True,True,0)
        
        # Plots ToolBar
        self.tbPlots = Gtk.Toolbar()
        self.tbPlots.set_name("tbPlots")
        self.tbPlots.set_icon_size(2)
        self.tbPlots.set_halign(Gtk.Align.START)
        self.btnPlotsAdd = Gtk.ToolButton()
        self.btnPlotsDel = Gtk.ToolButton()
        self.btnPlotsAdd.set_label("Add")
        self.btnPlotsDel.set_label("Remove")
        self.btnPlotsAdd.set_homogeneous(False)
        self.btnPlotsDel.set_homogeneous(False)
        self.tbPlots.insert(self.btnPlotsAdd,0)
        self.tbPlots.insert(self.btnPlotsDel,1)
        self.boxPlots.pack_start(self.tbPlots,False,True,0)
        
        # Plots Tree
        self.treePlots = GuiPlotsTree(self.theBook)
        self.boxPlots.pack_start(self.treePlots,True,True,0)
        
        return
    
# End Class GuiPlotsPane
