# -*- coding: utf-8 -*
"""novelWriter Init

 novelWriter – Init File
=========================
 Application initialisation

 File History:
 Created:   2017-01-10 [0.1.0]
 Rewritten: 2017-10-03 [0.4.0]

"""

import logging
import getopt
import gi

gi.require_version("Gtk","3.0")

from gi.repository import Gtk
from os            import path
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

#
#  Logging
# =========
#  Standard used for logging levels in novelWriter:
#    CRITICAL  Use for errors that result in termination of the program
#    ERROR     Use when an action fails, but execution continues
#    WARNING   When something unexpected, but non-critical happens
#    INFO      Any useful user information like open, save, exit initiated
#  ----------- SPAM Threshold : Output above should be minimal -----------------
#    DEBUG     Use for descriptions of main program flow
#    VERBOSE   Use for outputting values and program flow details
#    VVERBOSE  Use for describing what the user does, like clicks and entries
#

# Adding verbose and vverbose logging levels

VERBOSE  = 9
VVERBOSE = 8
logging.addLevelName(VERBOSE, "DEBUGV")
logging.addLevelName(VVERBOSE,"DEBUGVV")

def logVerbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kws) 
def logVVerbose(self, message, *args, **kws):
    if self.isEnabledFor(VVERBOSE):
        self._log(VVERBOSE, message, args, **kws) 

logging.Logger.verbose  = logVerbose
logging.Logger.vverbose = logVVerbose

# Initiating logging
logger = logging.getLogger(__name__)

#
#  Main Program
# ==============
#

# Load the main config as a global object
CONFIG = Config()

def main(sysArgs):
    """
    Parses command line, sets up logging, and launches main GUI.
    """
    
    # Valid Input Options
    shortOpt = "hd:qtl:v"
    longOpt  = [
        "help",
        "debug=",
        "verbose",
        "vverbose",
        "quiet",
        "time",
        "logfile=",
        "version",
    ]
    
    helpMsg = (
        "novelWriter {version} ({status})\n"
        "{copyright}\n"
        "\n"
        "Usage:\n"
        " -h, --help      Print this message.\n"
        " -d, --debug     Debug level. Valid options are DEBUG, INFO, WARN or ERROR.\n"
        "     --verbose   Increase verbosity of debug.\n"
        "     --vverbose  Increase verbosity of debug even more.\n"
        " -q, --quiet     Disable output to command line. Does not affect log file.\n"
        " -t, --time      Show time stamp in logging output. Adds milliseconds for verbose.\n"
        " -l, --logfile   Log file.\n"
        " -v, --version   Print program version and exit.\n"
    ).format(
        version   = __version__,
        status    = __status__,
        copyright = __copyright__
    )
    
    # Defaults
    debugLevel = logging.WARN
    debugStr   = "{levelname:8s}  {message}"
    timeStr    = "[{asctime}] "
    logFile    = ""
    toFile     = False
    toStd      = True
    showTime   = False
    
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
                debugStr   = "{lineno:4d}:{name:15s} {levelname:8s}  {message}"
            else:
                print("Invalid debug level")
                exit(2)
        elif inOpt in ("-l","--logfile"):
            logFile = inArg
            toFile  = True
        elif inOpt in ("-q","--quiet"):
            toStd = False
        elif inOpt in ("--verbose"):
            debugLevel = VERBOSE
            timeStr    = "[{asctime}.{msecs:03.0f}] "
        elif inOpt in ("--vverbose"):
            debugLevel = VVERBOSE
            timeStr    = "[{asctime}.{msecs:03.0f}] "
        elif inOpt in ("-t","--time"):
            showTime = True
        elif inOpt in ("-v", "--version"):
            print("makeNovel %s Version %s" % (__status__,__version__))
            exit()
    
    # Set Logging
    if showTime: debugStr = timeStr+debugStr
    logFmt = logging.Formatter(fmt=debugStr,datefmt="%Y-%m-%d %H:%M:%S",style="{")
    
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
