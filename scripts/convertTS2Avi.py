#!/usr/bin/env python
# -*- coding: latin1 -*-

'''
Convert M2TS to AVI
'''



## Import
import sys
import os
import time, datetime
import subprocess
from optparse import OptionParser

## common
from python_common import *
HEADER = "M2tsTOAvi"

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
errC = 0

###############################################





###############################################
###############################################
##                FUNCTIONS                  ##
###############################################
###############################################

def convertFile(fileList) :
    global dbg
    global errC
    dbg.info(HEADER, "In  convertFile")

    oldDir = os.getcwd()

    for (fileD, fileN, fileE) in fileList :
        dbg.info(HEADER, "In  convertFile directory " + str(fileD) + "  convertFile " + fileN + fileE)

        if (fileD != "") :
            os.chdir(fileD)

        cmd='ffmpeg -i "' + fileN + fileE + '" -threads 3 -r 29.97 -vcodec libxvid -s 1024x576 -aspect 16:9 -b 2000k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 "' + fileN + '.avi"'
        dbg.info(HEADER, "In  convertFile cmd=" + str(cmd))
        procPopen = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        procPopen.wait()
        if (procPopen.returncode != 0) :
            errC += 1
            dbg.error(HEADER, "In  convertFile file: issue with " + str(os.path.join(fileD, fileN + fileE)))

        if (fileD != "") :
            os.chdir(oldDir)

    dbg.info(HEADER, "Out convertFile")

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
    warnC = 0
    dbg.info(HEADER, "In  main")

    fileList = list()

    dbg.info(HEADER, "In  main parsedArgs=" + str(parsedArgs))
    dbg.info(HEADER, "In  main args=" + str(args))

    ## Create list of files
    extAuth=[".m2ts", ".M2TS"]
    (fileList, warnC) = listFromArgs(dbg, HEADER, args, extAuth)

    ## Verify if there is at least one video to convert
    if (len(fileList) == 0) :
        dialog_error("Convert M2TS files", "\nNo video has been found\n")
    else :
        dbg.info(HEADER, "In  main videos to convert = " + str(len(fileList)))

    ## Convert them
    convertFile(fileList)

    msg = "\nJob fini : " + str(len(fileList)) + " video a convertir.\n"
    if (warnC != 0) :
        msg += "\nWarning = " + str(warnC)
    if (errC != 0) :
        msg += "\nError = " + str(errC)
    msg += "\n\nLog file = " + str(logFile)
    dialog_info("Convert video", msg)
    
    dbg.info(HEADER, "Out main")

###############################################




if __name__ == '__main__':
 
    ## Create log class
    dbg = LOGC(logFile, HEADER, parsedArgs.debug, parsedArgs.gui)

    main()

