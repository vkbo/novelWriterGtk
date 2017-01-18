# -*- coding: utf-8 -*

##
#  novelWriter – Init File
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#  Application initialisation
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, GdkPixbuf
from os            import path
from datetime      import datetime
from nw.config     import Config

# ==================================================================================================================== #
# Begin Initialisation

logger.basicConfig(format="%(levelname)s: %(message)s",level=logger.DEBUG)

# Global Classes
CONFIG  = Config()
BUILDER = Gtk.Builder()

BUILDER.add_from_file(path.join(CONFIG.guiPath,"novelWriter.glade"))
CONFIG.setBuilder(BUILDER)
CONFIG.updateRecentList()

# End Initialisation
# ==================================================================================================================== #
# Begin Global Constant

# Date Formats
DATEFORMAT = {
    "dd.mm.yyyy" : ["DMY","."],
    "dd/mm/yyyy" : ["DMY","/"],
    "dd-mm-yyyy" : ["DMY","-"],
    "mm.dd.yyyy" : ["MDY","."],
    "mm/dd/yyyy" : ["MDY","/"],
    "mm-dd-yyyy" : ["MDY","-"],
    "yyyy.mm.dd" : ["YMD","."],
    "yyyy/mm/dd" : ["YMD","/"],
    "yyyy-mm-dd" : ["YMD","-"],
}
DATE_NUM1 = 0
DATE_NUM2 = 1
DATE_TIME = 2
DATE_DATE = 3
DATE_FULL = 4

# Tab Indices
MAIN_DETAILS = 0
MAIN_EDITOR  = 1
MAIN_SOURCE  = 2

# Scene Index Columns
SCIDX_TITLE   = 0
SCIDX_NUMBER  = 1
SCIDX_WORDS   = 2
SCIDX_SECTION = 3
SCIDX_CHAPTER = 4
SCIDX_COUNT   = 5

# Scene Sections
SCN_NONE = 0
SCN_PRO  = 1
SCN_CHAP = 2
SCN_EPI  = 3
SCN_ARCH = 4

# Word or Char Count
COUNT_ONLOAD = 0
COUNT_ADDED  = 1
COUNT_LATEST = 2

# Actions
ACTION_NONE   = 0
ACTION_CANCEL = 1
ACTION_LOAD   = 2
ACTION_SAVE   = 3
ACTION_EDIT   = 4
ACTION_NEW    = 5

# Editor Paste Type
PASTE_PLAIN = 0
PASTE_CLEAN = 1

# StatusBar LED Colours
LED_GREY   = "icon-grey"
LED_GREEN  = "icon-green"
LED_YELLOW = "icon-yellow"
LED_RED    = "icon-red"
LED_BLUE   = "icon-blue"

# End Global Constants
# ==================================================================================================================== #
# Begin Global Functions

def formatDateTime(dateFormat=DATE_NUM1, timeValue=None, localFormat="dd.mm.yyyy"):

    if timeValue is None: timeValue = datetime.now()

    if dateFormat == DATE_NUM1: return "{:%Y%m%d%H%M%S}".format(timeValue)
    if dateFormat == DATE_NUM2: return "{:%Y%m%d-%H%M%S}".format(timeValue)

    timeString = "{:%H%M%S}".format(timeValue)

    dtSeq = DATEFORMAT[localFormat][0]
    dtSep = DATEFORMAT[localFormat][1]

    if dtSeq == "DMY": dateString = "{:%d.%m.%Y}".format(timeValue)
    if dtSeq == "MDY": dateString = "{:%m.%d.%Y}".format(timeValue)
    if dtSeq == "YMD": dateString = "{:%Y.%m.%d}".format(timeValue)

    dateString.replace(".",dtSep)

    if dateFormat == DATE_TIME: return timeString
    if dateFormat == DATE_DATE: return dateString
    if dateFormat == DATE_FULL: return timeString+" "+dateString
    
    return None

def dateFromStamp(dateString):
    return datetime.strptime(dateString,"%Y%m%d%H%M%S")

def makeSortString(section,chapter,number):
    return "%01d.%02d.%03d" % (section,chapter,number)

def getIconWidget(iconID, iconSize):

    guiPath  = CONFIG.guiPath
    iconFile = "%s-%s.png" % (iconID, str(iconSize))
    iconPath = path.join(guiPath,"icons",iconFile)
    gtkImage = Gtk.Image()

    if path.isfile(iconPath):
        gtkImage.set_from_file(iconPath)
    else:
        iconFile = "%s-256.png" % iconID
        iconPath = path.join(guiPath,"icons",iconFile)
        if path.isfile(iconPath):
            pixBuffer = GdkPixbuf.Pixbuf.new_from_file(iconPath)
            gtkImage.set_from_pixbuf(pixBuffer.scale_simple(iconSize,iconSize,GdkPixbuf.InterpType.BILINEAR))
    
    return gtkImage

# End Global Functions
# ==================================================================================================================== #
