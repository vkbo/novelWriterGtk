# -*- coding: utf-8 -*

##
#  pyÉcrire – Global Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  This file holds all the global data manipulation functions
##

import logging as logger

from hashlib   import sha256
from datetime  import datetime
from re        import sub, compile
from unidecode import unidecode
from bleach    import clean

#
# Strips string of all non-English characters
#

def simplifyString(inStr):

    outStr = str(unidecode(inStr)).lower()
    outStr = sub("[^a-z0-9\.]","",outStr)

    return outStr

#
# Creates a file handle from a string
#

def makeHandle(inStr):

    tmpStr     = simplifyString(inStr)
    timeStamp  = makeTimeStamp(1)
    hashObject = sha256((tmpStr+timeStamp).encode())
    hexHandle  = hashObject.hexdigest()[:10]

    return hexHandle

#
# Create a TimeStamp string of a time or current time if none specified
#

def makeTimeStamp(stringFormat=0, timeStamp=None):

    if timeStamp is None:
        timeStamp = datetime.now()

    if   stringFormat == 0:
        return "{:%Y%m%d%H%M%S}".format(timeStamp)
    elif stringFormat == 1:
        return "{:%Y%m%d-%H%M%S}".format(timeStamp)
    elif stringFormat == 2:
        return "{:%Y-%m-%d %H:%M:%S}".format(timeStamp)
    elif stringFormat == 3:
        return "{:%d/%m/%Y %H:%M:%S}".format(timeStamp)
    elif stringFormat == 4:
        return "[{:%H:%M:%S}] ".format(timeStamp)
    else:
        return "{:%Y.%m.%d %H:%M:%S}".format(timeStamp)

    return ""

#
# Reformat Date from TimeStamp
#

def reformatDate(dateString):

    year   = dateString[0:4]
    month  = dateString[4:6]
    day    = dateString[6:8]

    hour   = dateString[9:11]
    minute = dateString[11:13]
    second = dateString[13:15]

    return "%s/%s/%s %s:%s:%s" % (day,month,year,hour,minute,second)

#
# Date String to Number
#

def dateFromString(dateString):
    return datetime.strptime(dateString,"%Y%m%d-%H%M%S")

#
# Format Time from Seconds
#

def formatTime(timeValue):

    minute, second = divmod(timeValue, 60)
    hour,   minute = divmod(minute, 60)

    return "%02d:%02d:%02d" % (hour, minute, second)

#
# Create Scene Number
#

def makeSceneNumber(group,section,chapter,number):
    return "%01s.%01d.%02d.%03d" % (group,section,chapter,number)

#
# Clean Up HTML Code
#

def htmlCleanUp(srcText):

    okTags   = ["p","b","i","u","strike"]
    okAttr   = {"*" : ["style"]}
    okStyles = ["text-align"]

    srcText  = clean(srcText,tags=okTags,attributes=okAttr,styles=okStyles,strip=True)

    if srcText[0:3] != "<p>": srcText = "<p>"+srcText+"</p>"

    srcText  = srcText.replace("<p></p>","")
    srcText  = srcText.replace("</p>","</p>\n")
    srcText  = srcText.replace('style=""',"")
    srcText  = srcText.replace("style=''","")
    srcText  = srcText.replace(" >",">")
    srcText  = srcText.replace("\n ","\n")

    return srcText

#
# Strip All HTML Code
#

def htmlStrip(srcText):

    okTags   = ["p"]
    okAttr   = {}
    okStyles = []

    srcText  = clean(srcText,tags=okTags,attributes=okAttr,styles=okStyles,strip=True)

    return srcText

#
# Word Count for HTML Files
#

def wordCount(srcHtml):

    regTags   = compile("<.*?>")
    cleanText = sub(regTags, " ", srcHtml)
    cleanText = cleanText.replace("&nbsp;", " ")
    cleanText = cleanText.strip()
    splitText = cleanText.split()

    return len(splitText), len(cleanText)

# End Functions
