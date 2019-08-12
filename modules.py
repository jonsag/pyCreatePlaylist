#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
videoTypes = (config.get('fileTypes', 'videoTypes')).split(',')  # allowed video file types
audioTypes = (config.get('fileTypes', 'audioTypes')).split(',')  # allowed audio file types

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode == 1:
        print(extra)
        usage(errorCode)
    elif errorCode == 2:
        print("No options given")
        usage(errorCode)
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])

    sys.exit(exitCode)