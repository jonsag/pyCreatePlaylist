#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import (onError, usage, outFile, videoTypes, audioTypes, 
                     checkOutFilePath, inDirCheck, findFiles, createPlaylist)


# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'o:i:e:msravh',
                                 ['outfile=', 
                                  'indir=',
                                  'extension=',
                                  'movies',
                                  'sound',  
                                  'recursive', 
                                  'absolute'
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
#if len(sys.argv) == 1:  # no options passed
#    onError(2, 2)
    
outDir = os.getcwd()
outFilePath = os.path.abspath(os.path.join(outDir, outFile))

inDir = outFilePath = os.path.abspath(os.getcwd())
checkInDir = False

recursive = False

findVideo = False
findAudio = False
extension = ""
extensionList = []

absolutePath = False

verbose = False
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-o', '--outfile'):
        outFilePath = argument
        outFilePath = os.path.abspath(outFilePath)
    elif option in ('-i', '--indir'):
        inDir = argument
        inDir = os.path.abspath(inDir)
        checkInDir = True
    elif option in ('-e', '--extension'):
        extension = argument
    elif option in ('-r', '--recursive'):
        recursive = True
    elif option in ('-m', '--movies'):
        findVideo = True
    elif option in ('-s', '--sound'):
        findAudio = True
    elif option in ('-a', '--absolute'):
        absolutePath = True
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
    
# outfile    
outDir, outFilePath, append = checkOutFilePath(outFilePath, verbose) # check all about the outfile path

# indir
if checkInDir:
    if inDirCheck(inDir, verbose):
        if verbose:
            print("+++ %s\n    is a directory" % inDir)
    else:
        onError(6, "%s\nis not a directory" % inDir)
        
# what to look for
if findVideo:
    extensionList.extend(videoTypes)
if findAudio:
    extensionList.extend(audioTypes)
if extension:
    extension = extension.split(',')
    extensionList.extend(extension)
    
# find files
files = findFiles(inDir, recursive, extensionList, verbose)

# create playlist
createPlaylist(files, outDir, outFilePath, absolutePath, append, verbose)








