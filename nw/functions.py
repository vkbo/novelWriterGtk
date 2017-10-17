# -*- coding: utf-8 -*
"""novelWriter Functions

 novelWriter – Functions
=========================
 Common functions for novelWriter

 File History:
 Created: 2017-02-22 [0.4.0]

"""

import logging
import nw
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, GdkPixbuf
from os            import path
from datetime      import datetime

logger = logging.getLogger(__name__)

def getTimeStamp(dateSep=""):
    timeValue  = datetime.now()
    returnDate = "{:%Y%m%d}".format(timeValue)
    returnTime = "{:%H%M%S}".format(timeValue)
    return "%s%s%s" % (returnDate,dateSep,returnTime)

def getIconWidget(iconID, iconSize=None):
    
    thmePath = path.join(nw.CONFIG.themePath,nw.CONFIG.theTheme)
    iconFile = "%s.svg" % iconID
    iconPath = path.join(thmePath,"icons",iconFile)
    gtkImage = Gtk.Image()
    
    if path.isfile(iconPath):
        gtkImage.set_from_file(iconPath)
    # else:
    #     iconFile = "%s-256.png" % iconID
    #     iconPath = path.join(guiPath,"icons",iconFile)
    #     if path.isfile(iconPath):
    #         pixBuffer = GdkPixbuf.Pixbuf.new_from_file(iconPath)
    #         gtkImage.set_from_pixbuf(pixBuffer.scale_simple(
    #             iconSize,iconSize,GdkPixbuf.InterpType.BILINEAR))
    
    return gtkImage
