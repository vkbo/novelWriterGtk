# -*- coding: utf-8 -*

##
#  novelWriter – Timer Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Main wrapper class for the GUI timer and its related functions
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, Gdk
from time          import time, strftime
from nw            import *

class Timer():

    def __init__(self):

        # Connect to GUI
        self.mainConf    = CONFIG
        self.getObject   = BUILDER.get_object

        self.timeSession = self.getObject("lblTimeSession")
        self.timeTotal   = self.getObject("lblTimeTotal")
        self.progTimer   = self.getObject("progTimerPause")
        self.timerStatus = self.getObject("lblTimerStatus")

        # Initialise Variables
        self.sessionTime = 0.0
        self.totalTime   = 0.0
        self.timeOffset  = time()
        self.timeBuffer  = 0.0
        self.prevTotal   = 0.0
        self.timerOn     = False
        self.tickCount   = 0
        self.autoPause   = self.mainConf.autoPause
        self.autoOffset  = 0.0
        self.autoTime    = 0.0

        self.timerStatus.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("#aa0000"))
        self.timerStatus.set_label("STOPPED")

        return

    ##
    #  Setters
    ##

    def setPreviousTotal(self, timeValue):
        self.prevTotal = timeValue
        self.timeTotal.set_label(self.formatTime(self.prevTotal))
        return

    ##
    #  Modifiers
    ##

    def updateTime(self):

        self.sessionTime = time() - self.timeOffset + self.timeBuffer
        self.totalTime   = self.sessionTime + self.prevTotal

        self.timeSession.set_label(self.formatTime(self.sessionTime))
        self.timeTotal.set_label(self.formatTime(self.totalTime))

        return

    def updateAutoTime(self):

        self.autoTime = time() - self.autoOffset
        self.progTimer.set_fraction(self.autoTime/self.autoPause)

        if self.autoTime >= self.autoPause:
            self.getObject("btnEditable").set_active(False)

        return

    ##
    #  Methods
    ##

    def resetAutoPause(self):

        self.autoOffset = time()
        self.progTimer.set_fraction(0.0)

        return

    def resetTimer(self):

        self.sessionTime = 0.0
        self.totalTime   = 0.0
        self.timeOffset  = time()
        self.timeBuffer  = 0.0
        self.prevTotal   = 0.0
        self.timerOn     = False
        self.tickCount   = 0
        self.autoOffset  = 0.0
        self.autoTime    = 0.0

        self.timeSession.set_label(self.formatTime(0))
        self.timeTotal.set_label(self.formatTime(0))

        return

    def startTimer(self):

        logger.debug("Timer: Started")

        self.timerOn    = True
        self.timeOffset = time()
        self.autoOffset = time()

        self.progTimer.set_fraction(0.0)

        self.timerStatus.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("#00aa00"))
        self.timerStatus.set_label("RUNNING")

        return

    def pauseTimer(self):

        logger.debug("Timer: Paused")

        self.timerOn    = False
        self.timeBuffer = self.timeBuffer + time() - self.timeOffset

        self.timerStatus.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("#ffaa00"))
        self.timerStatus.set_label("PAUSED")

        return

    def stopTimer(self):

        logger.debug("Timer: Stopped")

        self.timerOn    = False
        self.timeBuffer = 0.0

        self.timerStatus.modify_fg(Gtk.StateType.NORMAL,Gdk.color_parse("#aa0000"))
        self.timerStatus.set_label("STOPPED")

        return

    ##
    #  Event Handlers
    ##

    def onTick(self):

        self.tickCount += 1
        if self.timerOn:
            self.updateTime()
            if self.autoPause > 0.0:
                self.updateAutoTime()

        return True

    ##
    #  Internal Methods
    ##

    def formatTime(self, timeValue):

        minute, second = divmod(timeValue, 60)
        hour,   minute = divmod(minute, 60)

        return "%02d:%02d:%02d" % (hour, minute, second)

# End Class Timer
