# -*- coding: utf-8 -*

import logging as logger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit

from time import time,strftime

class Timer():

    def __init__(self, builder, config):

        # Connect to GUI
        self.guiBuilder = builder
        self.mainConf   = config
        self.getObject  = self.guiBuilder.get_object
        self.timeLabel  = self.getObject("lblTimeCount")
        self.progTimer  = self.getObject("progressTimer")
        self.btnStart   = self.getObject("btnTimerStart")
        self.btnPause   = self.getObject("btnTimerPause")
        self.btnStop    = self.getObject("btnTimerStop")
        self.timeOffset = time()
        self.timeBuffer = 0.0
        self.timerOn    = False
        self.tickCount  = 0
        self.autoPause  = self.mainConf.timeAutoPause
        self.autoOffset = 0.0
        self.autoTime   = 0.0

        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)

        logger.debug("Time offset %s" % self.timeOffset)



        return

    def onTick(self):
        self.tickCount += 1
        if self.timerOn:
            self.updateTime()
            if self.autoPause > 0.0:
                self.updateAutoTime()
        return True

    def updateTime(self):
        currTime = time() - self.timeOffset + self.timeBuffer
        m, s = divmod(currTime, 60)
        h, m = divmod(m, 60)
        self.timeLabel.set_label("%02d:%02d:%02d" % (h, m, s))
        return

    def updateAutoTime(self):
        self.autoTime = time() - self.autoOffset
        self.progTimer.set_fraction(self.autoTime/self.autoPause)
        if self.autoTime >= self.autoPause:
            self.onTimerPause()
        return

    def resetAutoPause(self):
        self.autoOffset = time()
        self.progTimer.set_fraction(0.0)
        return

    def onTimerStart(self,guiObject=None):
        logger.debug("Timer started")
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
        self.timerOn    = False
        self.timeBuffer = self.timeBuffer + time() - self.timeOffset
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(True)
        return

    def onTimerStop(self,guiObject=None):
        logger.debug("Timer stopped")
        self.timerOn    = False
        self.timeBuffer = 0.0
        self.btnStart.set_sensitive(True)
        self.btnPause.set_sensitive(False)
        self.btnStop.set_sensitive(False)
        return

