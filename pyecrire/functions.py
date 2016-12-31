# -*- coding: utf-8 -*

import logging as logger
from hashlib     import sha256
from datetime    import datetime
from re          import sub
from unicodedata import normalize

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
    else:
        return "{:%Y.%m.%d %H:%M:%S}".format(timeStamp)

    return ""



