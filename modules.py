#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
videoTypes = (config.get('fileTypes', 'videoTypes')).split(',')  # allowed video file types
audioTypes = (config.get('fileTypes', 'audioTypes')).split(',')  # allowed audio file types

outFileName = config.get('output', 'outFileName')
outFileExtension = config.get('output', 'outFileExtension')
outFile = "%s.%s" % (outFileName, outFileExtension)

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode == 1: # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode == 2: # no argument given to option, print usage and exit
        print("No options given")
        usage(errorCode)
    elif errorCode == 3: # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4: # print error information and return running program
        print(extra)
        return
            
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])

    sys.exit(exitCode)