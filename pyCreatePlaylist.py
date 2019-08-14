#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import (onError, usage, outFile, outFileExtension, 
                     checkOutFilePath, inDirCheck)

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'o:i:rvh',
                                 ['outfile=', 
                                  'indir=', 
                                  'recursive'
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
    elif option in ('-r', '--recursive'):
        recursive = True
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
    
# outfile    
outFilePath = checkOutFilePath(outFilePath, verbose) # check all about the outfile path

# indir
if checkInDir:
    if inDirCheck(inDir, verbose):
        if verbose:
            print("+++ %s\n    is a directory" % inDir)
    else:
        onError(6, "%s\nis not a directory" % inDir)

if recursive:
    print("\nScanning directory:\n%s\nrecursively..." % inDir)
else:
    print("\nScanning directory:\n%s ..." % inDir)
    
