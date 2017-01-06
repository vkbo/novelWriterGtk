# -*- coding: utf-8 -*

##
#  pyÉcrire – Timer Class
# ~~~~~~~~~~~~~~~~~~~~~~~~
#  Main class for the session timer
##

import logging as logger

import gi
gi.require_version('Gtk', '3.0')

from gi.repository      import Gtk
from time               import time, strftime
from pyecrire.functions import makeTimeStamp, formatTime

class Timer():

    def __init__(self, builder, config):

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object

        self.timeLabel  = self.getObject("lblTimeCount")
        self.docSLabel  = self.getObject("lblDTSessionTime")
        self.docTLabel  = self.getObject("lblDTTotalTime")
        self.progTimer  = self.getObject("progressTimer")
        self.btnStart   = self.getObject("btnTimerStart")
        self.btnPause   = self.getObject("btnTimerPause")
        self.btnStop    = self.getObject("btnTimerStop")

        self.statusBar  = self.getObject("mainStatus")
        self.statusCID  = self.statusBar.get_context_id("Timer")

        # Initialise Variables
        self.timeOffset = time()
        self.timeBuffer = 0.0
        self.timerOn    = False
        self.tickCount  = 0
        self.autoPause  = self.mainConf.autoPause
        self.autoOffset = 0.0
        self.autoTime   = 0.0
        self.docOffset  = time()
        self.docBuffer  = 0.0
        self.docTotal   = 0.0
        self.docTimerOn = False

        # Default Button States
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)

        return

    def setDocTotal(self, timeValue):
        self.docTotal = timeValue
        return

    def updateTime(self):

        currTime = time() - self.timeOffset + self.timeBuffer
        docTime  = time() - self.docOffset  + self.docBuffer

        self.timeLabel.set_label(formatTime(currTime))
        self.docSLabel.set_label(formatTime(docTime))
        self.docTLabel.set_label(formatTime(docTime+self.docTotal))

        return

    def updateAutoTime(self):
        self.autoTime = time() - self.autoOffset
        self.progTimer.set_fraction(self.autoTime/self.autoPause)
        if self.autoTime >= self.autoPause:
            self.onTimerPause()
            self.docTimerPause()
            self.statusBar.pop(self.statusCID)
            self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer auto-paused")
        return

    def resetAutoPause(self):
        self.autoOffset = time()
        self.progTimer.set_fraction(0.0)
        return

    def docTimerPause(self):
        self.docTimerOn = False
        self.docBuffer  = self.docBuffer + time() - self.docOffset
        return

    def onTick(self):
        self.tickCount += 1
        if self.timerOn:
            self.updateTime()
            if self.autoPause > 0.0:
                self.updateAutoTime()
        return True

    def onTimerStart(self,guiObject=None):
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

    def onTimerPause(self,guiObject=None):
        logger.debug("Timer paused")
        self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer paused")
        self.timerOn    = False
        self.timeBuffer = self.timeBuffer + time() - self.timeOffset
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(True)
        return

    def onTimerStop(self,guiObject=None):
        logger.debug("Timer stopped")
        self.statusBar.push(self.statusCID,makeTimeStamp(4)+"Session timer stopped")
        self.timerOn    = False
        self.timeBuffer = 0.0
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)
        return

# End Class Timer
