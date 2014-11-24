#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Send file(s) to DL FREE from nemo
'''



## Import
import sys
import os
import re
import time, datetime
from subprocess import Popen, PIPE
from optparse import OptionParser

## common
from python_common import *
HEADER = "FTP_FREE"

## directory
logDir   = getLogDir()

###############################################



###############################################
###############################################
##              Line Parsing                 ##
###############################################
###############################################

parsedArgs = {}
parser = OptionParser()


parser.add_option(
    "--debug",
    action  = "store_true",
    dest    = "debug",
    default = False,
    help    = "Display all debug information"
    )

parser.add_option(
    "--nogui",
    action  = "store_false",
    dest    = "gui",
    default = True,
    help    = "Print information in a shell"
    )

(parsedArgs , args) = parser.parse_args()

###############################################



###############################################
## Global variables
###############################################

t = str(datetime.datetime.today().isoformat("_"))
logFile = os.path.join(logDir, HEADER + "_" + t + ".log")

###############################################





###############################################
###############################################
###############################################
##                 MAIN                      ##
###############################################
###############################################
###############################################


def main() :
    global dbg
    dbg.info(HEADER, "In  main")

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    if args.__len__() != 1 :
        dialog_error("Send File to DL Free", "Only 1 file supported")
        sys.exit(-1)

    fileN = ""
    if (os.path.isfile(args[0])) :
        fileN = args[0]
    else :
        dialog_error("Send File to DL Free", args[0] + " is not a file")
        sys.exit(-1)

    ## Launch the ftp free program
    out = ""
    err = ""
    cmdToLaunch=getBinDir() + '/ftp-free "' + str(fileN) + '"'
    dbg.info(HEADER, "In  main cmdToLaunch=" + str(cmdToLaunch))
    procPopen = Popen(cmdToLaunch, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = procPopen.communicate()
    dbg.info(HEADER, "In  main result out\n" + str(out))
    dbg.info(HEADER, "In  main result err\n" + str(err))

    ## Print result
    msg = "Fichier envoyé : " + str(fileN) + "\n\n"
    if re.search("Fichier d'origine :", out) :
        msg += "URL de download: " + "\n"
        msg += "    " + re.findall("URL Fichier depose : (.*)", out)[0] + "\n"
    if re.search("URL pour suppression du fichier :", out) :
        msg += "URL de suppression: " + "\n"
        msg += "    " + re.findall("URL pour suppression du fichier : (.*)", out)[0] + "\n"
    
    if (err != "") :
        dialog_error("Send File to DL Free", msg)
    else :
        dialog_info("Send File to DL Free", msg)

    ## Send email
    dbg.info(HEADER, "In  main send mail")
    dbg.info(HEADER, "In  main send mail args[0].encode=" + str(args[0].encode('latin1')))
    dbg.info(HEADER, "In  main send mail msg.encode=" + str(msg.encode('latin1')))
    try:
        sendMail("gregory.brancq@free.fr", "gregory.brancq@free.fr", "", "Send to DL Free : " + str(args[0].encode('latin1')), msg.encode('latin1'));
    except :
        dbg.error(HEADER, "In  main send mail issue ")

    dbg.info(HEADER, "Out main")



if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()

###############################################
