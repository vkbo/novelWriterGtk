# -*- coding: utf-8 -*
"""novelWriter GUI TimeLine

 novelWriter – GUI TimeLine
============================
 Class holding the book time line view

 File History:
 Created: 2017-11-02 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository      import Gtk

logger = logging.getLogger(__name__)

class GuiTimeLine(Gtk.DrawingArea):
    
    def __init__(self, theBook):
        
        Gtk.DrawingArea.__init__(self)
        
        self.theBook = theBook
        
        self.set_name("drawTimeLine")
        self.connect("draw", self.onExpose)
        
        return
    
    def onExpose(self, guiObject, guiCtx):
        
        guiCtx.set_line_width(2)
        guiCtx.set_source_rgb(0.9,0.0,0.6)
        guiCtx.rectangle(10,10,100,100)
        guiCtx.stroke()
        
        return
    
# End Class GuiTimeLine
