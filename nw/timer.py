# -*- coding: utf-8 -*

##
#  novelWriter – Timer Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Main wrapper class for the GUI timer and its related functions
##

import logging as logger

import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from time          import time, strftime
from nw            import *

class Timer():

    def __init__(self):

        # Connect to GUI
        self.mainConf   = CONFIG
        self.getObject  = BUILDER.get_object

        self.timeLabel  = self.getObject("lblTimeCount")
        self.timeTotal  = self.getObject("lblTimeTotal")
        self.progTimer  = self.getObject("progressTimer")
        self.btnStart   = self.getObject("btnTimerStart")
        self.btnPause   = self.getObject("btnTimerPause")
        self.btnStop    = self.getObject("btnTimerStop")

        self.statusBar  = self.getObject("mainStatus")
        self.statusCID  = self.statusBar.get_context_id("Timer")

        # Initialise Variables
        self.currTime   = 0.0
        self.totTime    = 0.0
        self.timeOffset = time()
        self.timeBuffer = 0.0
        self.docTotal   = 0.0
        self.timerOn    = False
        self.tickCount  = 0
        self.autoPause  = self.mainConf.autoPause
        self.autoOffset = 0.0
        self.autoTime   = 0.0

        # Default Button States
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)

        return

    def setDocTotal(self, timeValue):
        self.docTotal = timeValue
        self.timeTotal.set_label(formatTime(self.docTotal))
        return

    def updateTime(self):

        self.currTime = time() - self.timeOffset + self.timeBuffer
        self.totTime  = self.currTime + self.docTotal

        self.timeLabel.set_label(formatTime(self.currTime))
        self.timeTotal.set_label(formatTime(self.totTime))

        return

    def updateAutoTime(self):

        self.autoTime = time() - self.autoOffset
        self.progTimer.set_fraction(self.autoTime/self.autoPause)

        if self.autoTime >= self.autoPause:
            self.pauseTimer()
            self.getObject("btnEditFile").set_active(False)
            self.statusBar.pop(self.statusCID)
            self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer auto-paused")

        return

    def resetAutoPause(self):

        self.autoOffset = time()
        self.progTimer.set_fraction(0.0)

        return

    def resetTimer(self):

        self.currTime   = 0.0
        self.totTime    = 0.0
        self.timeOffset = time()
        self.timeBuffer = 0.0
        self.docTotal   = 0.0
        self.timerOn    = False
        self.tickCount  = 0
        self.autoOffset = 0.0
        self.autoTime   = 0.0

        self.timeLabel.set_label(formatTime(0))
        self.timeTotal.set_label(formatTime(0))

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

    def startTimer(self):

        if not self.btnStart.get_sensitive(): return
        logger.debug("Timer started")

        self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer started")
        self.timerOn    = True
        self.timeOffset = time()
        self.autoOffset = time()
        self.btnStart.set_sensitive(False)
        self.btnPause.set_sensitive(True)
        self.btnStop.set_sensitive(True)
        self.progTimer.set_fraction(0.0)

        return

    def pauseTimer(self):

        if not self.btnPause.get_sensitive(): return
        logger.debug("Timer paused")

        self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer paused")
        self.timerOn    = False
        self.timeBuffer = self.timeBuffer + time() - self.timeOffset
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(True)

        return

    def stopTimer(self):

        if not self.btnStop.get_sensitive(): return
        logger.debug("Timer stopped")

        self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer stopped")
        self.timerOn    = False
        self.timeBuffer = 0.0
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)

        return

# End Class Timer
