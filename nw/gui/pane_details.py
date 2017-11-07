# -*- coding: utf-8 -*
"""novelWriter Doc Details Class

 novelWriter – Doc Details Class
=================================
 Main wrapper class for the GUI doc details

 File History:
 Created:   2017-10-06 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, Pango
from os            import path

logger = logging.getLogger(__name__)

class GuiDocDetails(Gtk.Alignment):
    
    def __init__(self):
        
        Gtk.Alignment.__init__(self)
        
        self.set_name("alignDetailsEdit")
        self.set_padding(40,20,10,40)
        
        self.boxOuter = Gtk.Box()
        self.boxOuter.set_name("boxDetailsOuter")
        self.boxOuter.set_orientation(Gtk.Orientation.VERTICAL)
        self.boxOuter.set_spacing(0)
        self.add(self.boxOuter)
        
        self.lblTitle = Gtk.Label()
        self.lblTitle.set_name("lblDetailsTitle")
        self.lblTitle.set_label("Details")
        self.lblTitle.set_xalign(0.0)
        self.lblTitle.set_margin_bottom(12)
        self.boxOuter.pack_start(self.lblTitle,False,False,0)
        
        # Details Toolbar
        self.tbDetails = Gtk.Toolbar()
        self.tbDetails.set_name("tbDetails")
        self.tbDetails.set_icon_size(Gtk.IconSize.MENU)
        self.tbDetails.set_margin_bottom(8)
        self.btnEditDetails = Gtk.ToolButton(icon_name="text-editor-symbolic")
        self.tbDetails.insert(self.btnEditDetails,0)
        self.tbDetails.insert(Gtk.SeparatorToolItem(),1)
        self.boxOuter.pack_start(self.tbDetails,False,True,0)
        
        self.scrollGrid = Gtk.ScrolledWindow()
        self.boxOuter.pack_start(self.scrollGrid,True,True,0)
        
        self.gridDetails = Gtk.Grid()
        self.gridDetails.set_name("gridDetails")
        self.gridDetails.set_row_spacing(4)
        self.gridDetails.set_column_spacing(12)
        
        rowNum     = 0
        rowLabels  = ["POV","Character(s)","Plot(s)"]
        rowWidgets = [
            Gtk.Label("None"),
            Gtk.Label("None"),
            Gtk.Label("None"),
        ]
        for rowLabel, rowWidget in zip(rowLabels,rowWidgets):
            rowNum += 1
            tmpLabel = Gtk.Label()
            tmpLabel.set_markup("<b>%s:</b>" % rowLabel)
            tmpLabel.set_xalign(0.0)
            self.gridDetails.attach(tmpLabel,1,rowNum,1,1)
            self.gridDetails.attach(rowWidget,2,rowNum,1,1)
        
        self.scrollGrid.add(self.gridDetails)
        
        return
    
# End Class GuiDocDetails
