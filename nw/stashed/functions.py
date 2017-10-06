# -*- coding: utf-8 -*
"""novelWriter Functions

novelWriter – Functions
=======================
Common functions for novelWriter

File History:
Created: 2017-02-22 [0.4.0]

"""

import logging as logger
import nw
import gi

gi.require_version("Gtk","3.0")

from gi.repository import Gtk, GdkPixbuf
from os            import path
from datetime      import datetime

def formatDateTime(dateFormat=nw.DATE_NUM1, timeValue=None, localFormat="dd.mm.yyyy"):

    dateDict = {
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

    if timeValue is None: timeValue = datetime.now()

    if dateFormat == nw.DATE_NUM1: return "{:%Y%m%d%H%M%S}".format(timeValue)
    if dateFormat == nw.DATE_NUM2: return "{:%Y%m%d-%H%M%S}".format(timeValue)

    timeString = "{:%H%M%S}".format(timeValue)

    dtSeq = dateDict[localFormat][0]
    dtSep = dateDict[localFormat][1]

    if dtSeq == "DMY": dateString = "{:%d.%m.%Y}".format(timeValue)
    if dtSeq == "MDY": dateString = "{:%m.%d.%Y}".format(timeValue)
    if dtSeq == "YMD": dateString = "{:%Y.%m.%d}".format(timeValue)

    dateString.replace(".",dtSep)

    if dateFormat == nw.DATE_TIME: return timeString
    if dateFormat == nw.DATE_DATE: return dateString
    if dateFormat == nw.DATE_FULL: return timeString+" "+dateString

    return None

def dateFromStamp(dateString):
    return datetime.strptime(dateString,"%Y%m%d%H%M%S")

def makeSortString(section,chapter,number):
    return "%01d.%02d.%03d" % (section,chapter,number)

def getIconWidget(iconID, iconSize):

    guiPath  = nw.CONFIG.guiPath
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
            gtkImage.set_from_pixbuf(pixBuffer.scale_simple(
                iconSize,iconSize,GdkPixbuf.InterpType.BILINEAR))

    return gtkImage

def formatTime(timeValue):

    minute, second = divmod(timeValue, 60)
    hour,   minute = divmod(minute, 60)

    return "%02d:%02d:%02d" % (hour, minute, second)
