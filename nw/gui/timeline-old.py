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

from gi.repository import Gtk
from nw.file.book  import BookItem

logger = logging.getLogger(__name__)

class GuiTimeLine(Gtk.DrawingArea):
    
    def __init__(self, theBook):
        
        Gtk.DrawingArea.__init__(self)
        
        self.theBook = theBook
        self.tblRows = []
        self.tblCols = []
        
        self.loadContent()
        
        self.set_name("drawTimeLine")
        self.connect("draw", self.onExpose)
        
        return
    
    def loadContent(self):
        
        self.tblRows = []
        self.tblCols = []
        
        tmpChars = []
        tmpPlots = []
        
        for treeHandle in self.theBook.theTree.treeOrder:
            
            treeItem   = self.theBook.getItem(treeHandle)
            
            itemHandle = treeItem["handle"]
            itemParent = treeItem["parent"]
            itemLevel  = treeItem["entry"].itemLevel
            itemClass  = treeItem["entry"].itemClass
            itemType   = treeItem["entry"].itemType
            
            if itemLevel == BookItem.LEV_ITEM:
                if itemType == BookItem.TYP_CHAR:
                    tmpChars.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
                elif itemType == BookItem.TYP_PLOT:
                    tmpPlots.append({
                        "handle" : itemHandle,
                        "name"   : treeItem["entry"].itemName,
                    })
            elif itemLevel == BookItem.LEV_FILE:
                if itemType == BookItem.TYP_BOOK:
                    treeParent  = self.theBook.getItem(itemParent)
                    itemSubType = treeParent["entry"].itemSubType
                    if itemSubType in (BookItem.SUB_PRO,BookItem.SUB_CHAP,BookItem.SUB_EPI):
                        self.tblCols.append({
                            "handle"    : itemHandle,
                            "name"      : treeItem["entry"].itemName,
                            "parhandle" : itemParent,
                            "partype"   : treeParent["entry"].itemSubType,
                            "parnum"    : treeParent["entry"].itemNumber,
                        })
        
        self.tblRows = tmpChars+tmpPlots
        
        return
    
    def onExpose(self, guiObject, guiCtx):
        
        self.loadContent()
        logger.vverbose("TimeLine: Redrawing")
        
        xOffset = 10
        yOffset = 30
        wScene  = 50
        hRow    = 20
        
        guiCtx.set_line_width(1)
        
        xPos = xOffset
        yPos = yOffset+2*hRow
        
        guiCtx.set_font_size(12)
        for rowItem in self.tblRows:
            guiCtx.move_to(xPos,yPos)
            guiCtx.set_source_rgba(1.0,1.0,1.0,1.0)
            guiCtx.show_text(rowItem["name"])
            yPos += hRow
        
        xPos    += 100
        yPos     = yOffset
        currChap = None
        scnCount = 0
        totCount = 0
        for colItem in self.tblCols:
            
            totCount += 1
            scnCount += 1
            
            guiCtx.move_to(xPos,yPos+hRow)
            guiCtx.set_source_rgba(1.0,1.0,1.0,1.0)
            guiCtx.show_text("SCN %d" % scnCount)
            # guiCtx.rectangle(xPos,yPos+2*hRow,wScene,100)
            # guiCtx.stroke()
            
            xPos += wScene
            if currChap is None: currChap = colItem["parhandle"]
            if not colItem["parhandle"] == currChap or totCount == len(self.tblCols):
                xChap = xPos-scnCount*wScene
                yChap = yOffset
                wChap = xPos-xChap
                hChap = hRow*(len(self.tblRows)+1)
                guiCtx.move_to(xChap,yChap)
                guiCtx.set_source_rgba(1.0,1.0,1.0,1.0)
                if colItem["partype"] == BookItem.SUB_CHAP:
                    guiCtx.show_text("%s %d" % (colItem["partype"],colItem["parnum"]))
                else:
                    guiCtx.show_text("%s" % colItem["partype"])
                guiCtx.set_source_rgba(1.0,1.0,1.0,0.5)
                guiCtx.rectangle(xChap,yChap+5,wChap,hChap)
                guiCtx.stroke()
                currChap = colItem["parhandle"]
                scnCount = 0
        
        return
    
# End Class GuiTimeLine
