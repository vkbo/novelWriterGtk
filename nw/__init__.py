# -*- coding: utf-8 -*
"""novelWriter Init

novelWriter – Init File
=======================
Application initialisation

File History:
Created: 2017-01-10 [0.1.0]

"""

import logging
import getopt
import gi

gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
from textwrap      import dedent
from nw.config     import Config
from nw.main       import NovelWriter

__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2016-2017, Veronica Berglyd Olsen"
__credits__    = ["Veronica Berglyd Olsen"]
__license__    = "GPLv3"
__version__    = "0.4.0"
__date__       = "2017"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "code@vkbo.net"
__status__     = "Development"

# ================================================================================================ #
# Begin Initialisation

# Logging
logger  = logging.getLogger(__name__)

# Global Classes
CONFIG  = Config()
BUILDER = Gtk.Builder()

BUILDER.add_from_file(path.join(CONFIG.appPath,"gui.xml"))
CONFIG.setBuilder(BUILDER)
# CONFIG.updateRecentList()

# End Initialisation
# ================================================================================================ #
# Begin Global Constant

# Date Formats
# DATE_NUM1 = 0
# DATE_NUM2 = 1
# DATE_TIME = 2
# DATE_DATE = 3
# DATE_FULL = 4

# Tab Indices
# MAIN_DETAILS = 0
# MAIN_EDITOR  = 1
# MAIN_SOURCE  = 2

# Scene Index Columns
# SCIDX_TITLE   = 0
# SCIDX_NUMBER  = 1
# SCIDX_WORDS   = 2
# SCIDX_SECTION = 3
# SCIDX_CHAPTER = 4
# SCIDX_TIME    = 5
# SCIDX_COUNT   = 6

# Scene Sections
# SCN_NONE = 0
# SCN_PRO  = 1
# SCN_CHAP = 2
# SCN_EPI  = 3
# SCN_ARCH = 4

# Word or Char Count
# COUNT_ONLOAD = 0
# COUNT_ADDED  = 1
# COUNT_LATEST = 2

# Actions
# ACTION_NONE   = 0
# ACTION_CANCEL = 1
# ACTION_LOAD   = 2
# ACTION_SAVE   = 3
# ACTION_EDIT   = 4
# ACTION_NEW    = 5

# Editor Paste Type
# PASTE_PLAIN = 0
# PASTE_CLEAN = 1

# StatusBar LED Colours
# LED_GREY   = "icon-grey"
# LED_GREEN  = "icon-green"
# LED_YELLOW = "icon-yellow"
# LED_RED    = "icon-red"
# LED_BLUE   = "icon-blue"

# End Global Constants
# ================================================================================================ #

#
# Main program
#

def main(sysArgs):
    
    # Valid Input Options
    shortOpt = "hd:ql:v"
    longOpt  = [
        "help",
        "debug=",
        "quiet",
        "logfile=",
        "version",
    ]
    
    helpMsg = dedent("""
        novelWriter %s (%s)
        %s
        
        Usage:
        -h, --help     Print this message.
        -d, --debug    Debug level. Valid options are DEBUG, INFO, WARN or ERROR.
        -q, --quiet    Disable output to command line.
        -l, --logfile  Log file.
        -v, --version  Print program version and exit.
        """ % (__version__,__status__,__copyright__)
    )
    
    # Defaults
    debugLevel = logging.WARN
    debugStr   = "[{asctime}] {levelname:8s}  {message}"
    logFile    = ""
    toFile     = False
    toStd      = True
    
    # Parse Options
    try:
        inOpts, inArgs = getopt.getopt(sysArgs,shortOpt,longOpt)
    except getopt.GetoptError:
        print(helpMsg)
        exit(2)
    
    for inOpt, inArg in inOpts:
        if   inOpt in ("-h","--help"):
            print(helpMsg)
            exit()
        elif inOpt in ("-d", "--debug"):
            if   inArg == "ERROR":
                debugLevel = logging.ERROR
            elif inArg == "WARN":
                debugLevel = logging.WARNING
            elif inArg == "INFO":
                debugLevel = logging.INFO
            elif inArg == "DEBUG":
                debugLevel = logging.DEBUG
                debugStr   = "[{asctime}] {lineno:4d}:{name:15s} {levelname:8s}  {message}"
            else:
                print("Invalid debug level")
                exit(2)
        elif inOpt in ("-l","--logfile"):
            logFile = inArg
            toFile  = True
        elif inOpt in ("-q","--quiet"):
            toStd = False
        elif inOpt in ("-v", "--version"):
            print("makeNovel %s Version %s" % (__status__,__version__))
            exit()
    
    # Set Logging
    logFmt  = logging.Formatter(fmt=debugStr,datefmt="%Y-%m-%d %H:%M:%S",style="{")
    # cHandle = logging.StreamHandler()
    
    if not logFile == "" and toFile:
        if path.isfile(logFile+".bak"):
            remove(logFile+".bak")
        if path.isfile(logFile):
            rename(logFile,logFile+".bak")
        
        fHandle = logging.FileHandler(logFile)
        fHandle.setLevel(debugLevel)
        fHandle.setFormatter(logFmt)
        logger.addHandler(fHandle)
    
    if toStd:
        cHandle = logging.StreamHandler()
        cHandle.setLevel(debugLevel)
        cHandle.setFormatter(logFmt)
        logger.addHandler(cHandle)
    
    logger.setLevel(debugLevel)

    NovelWriter()
    Gtk.main()
    
    return
