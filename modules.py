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
    elif errorCode in (3, 5, 6): # print error information and exit
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
    
def checkOutFilePath(outFilePath, verbose):
    # handle outfile
    # handle directory
    if os.path.isdir(outFilePath): # check if outfile is a directory
        if verbose:
            print("+++ You stated a directory as output")
        outDir = os.path.abspath(outFilePath)
        if not os.access(os.path.abspath(outDir), os.W_OK): # check for write permission
            onError(5, "You do not have write permission to:\n%s" % os.path.abspath(outDir))
        outFilePath = os.path.join(outFilePath, outFile)
    else:
        outDir = os.path.dirname(outFilePath) # extract directory from path
        if verbose:
            print("--- Checking directory: %s" % outDir)
        if not os.path.isdir(outDir): # check if out directory exists
            onError(4, "Directory does not exist")
            createDir = raw_input("Do you wish to create it?\n(Y/n) ")
            if createDir == "n" or createDir == "N":
                print("Exiting...")
                sys.exit(0)
            else:
                dirAbove = os.path.dirname(outDir) # get directory above out directory
                if not os.access(os.path.abspath(dirAbove), os.W_OK): # check for write permission
                    onError(3, "You do not have write permission to:\n%s" % os.path.abspath(dirAbove))
                    
                if verbose:
                    print("+++ Creating directory...")
                    os.mkdir(outDir)
                outDir = os.path.abspath(outDir)
    if verbose:
        print("+++ Outdir: %s" % outDir)
        print("+++ Outfile: %s" % os.path.basename(outFilePath))
    # handle file
    if not "." in (os.path.basename(outFilePath)):
        if verbose:
            print("+++ Filename does not have an extension\n    Adding .%s ..." % outFileExtension)
        outFilePath = "%s.%s" % (outFilePath, outFileExtension)
    
    print("\nPlaylist will be created at:\n%s" % outFilePath)
    
def inDirCheck(inDir, verbose):
    if verbose:
        print("--- Checking in directory...")
    isDir = False
    if os.path.isdir(inDir): # check if inDir is a directory
        isDir = True
    
    return isDir

