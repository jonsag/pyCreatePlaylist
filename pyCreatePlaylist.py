#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import onError, usage, outFile, outFileExtension

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'o:vh',
                                 ['outfile=', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
outDir = os.getcwd()
outFilePath = os.path.join(outDir, outFile)

verbose = False
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-o', '--outfile'):
        outFilePath = argument
        outFilePath = os.path.abspath(outFilePath)
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
        
# handle outfile
# handle directory
if os.path.isdir(outFilePath): # check if outfile is a directory
    print("+++ You stated a directory as output")
    outDir = os.path.abspath(outFilePath)
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
                onError(3, "No write permission to create directory")
                
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
if verbose:
    print("+++ Playlist will be created at:\n%s" % outFilePath)
    
