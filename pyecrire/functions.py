# -*- coding: utf-8 -*

##
#  pyÉcrire – Global Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Various functions used in the applications
##

import logging as logger

from hashlib     import sha256
from datetime    import datetime
from re          import sub, compile
from unicodedata import normalize
from bleach      import clean

#
# Strips string of all non-English characters
#

def simplifyString(inStr):

    outStr = normalize("NFKD",inStr.decode("utf-8")).encode("ASCII","ignore").lower()
    outStr = sub("[^a-z0-9\.]","",outStr)

    return outStr


#
# Creates a file handle from a string
#

def makeHandle(inStr):

    tmpStr     = simplifyString(inStr)
    timeStamp  = makeTimeStamp(1)
    hashObject = sha256(tmpStr+timeStamp)
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
# Create Scene Number
#

def makeSceneNumber(group,section,chapter,number):
    return "%01s.%01d.%02d.%03d" % (group,section,chapter,number)


#
# Clean Up HTML Code
#

def htmlCleanUp(srcText):

    okTags   = ["p","b","i","u"]
    okAttr   = {"*" : ["style"]}
    okStyles = ["color","text-align"]

    srcText  = clean(srcText,tags=okTags,attributes=okAttr,styles=okStyles)

    srcText  = srcText.replace("</p>","</p>\n")
    srcText  = srcText.replace('style=""',"")
    srcText  = srcText.replace("style=''","")
    srcText  = srcText.replace(" >",">")
    srcText  = srcText.replace("\n ","\n")

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

    return len(splitText)

# End Functions
