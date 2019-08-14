#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys, glob
from audioop import add

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
    elif errorCode in (3, 5, 6, 7, 8, 9, 11): # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode in (4, 10): # print error information and return running program
        print(extra)
        return
            
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])

    sys.exit(exitCode)
    
def checkOutFilePath(outFilePath, verbose):    
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
            onError(4, "\nDirectory does not exist")
            createDir = input("Do you wish to create it?\n(Y/n) ")
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
    append = True
    
    if not "." in (os.path.basename(outFilePath)): # check if there is a file extension
        if verbose:
            print("+++ Filename does not have an extension\n    Adding .%s ..." % outFileExtension)
    
        outFilePath = "%s.%s" % (outFilePath, outFileExtension)
        
    if os.path.isfile(outFilePath):
        onError(10, "\nFile \n%s\nexists" % outFilePath)
        f = open(outFilePath, "r") # open file for reading
        if f.mode == 'r': # check if file is in read mode
            contents = f.read()
            print("----------\n" + contents + "----------\n") # print file
            f.close
        else:
            onError(11, "Could not open file for reading")
                
        questionAppend = input("Do you wish to 'a'ppend to it, 'o'verwrite or 'e'xit?\n(A/o/e) ")
        if questionAppend == "o" or questionAppend == "O":
            append = False
            if verbose:
                print("--- Removing old file...")
            os.remove(outFilePath)
        elif questionAppend == "e" or questionAppend == "E":
            print("Exiting...")
            sys.exit(0)
    
    print("\nPlaylist will be saved to:\n%s" % outFilePath)
    
    return outDir, outFilePath, append
    
def inDirCheck(inDir, verbose):
    if verbose:
        print("--- Checking in directory...")
    
    isDir = False       
    
    if os.path.isdir(inDir): # check if inDir is a directory
        isDir = True
        
    if not os.access(os.path.abspath(inDir), os.R_OK): # check if we have read permissions
        onError(7, "You do not have read permission to\n%s" % inDir) 
    
    return isDir

def addS(stringList):
    add = ""
    
    if len(stringList) >= 2 or len(stringList) == 0:
        add = "s"
        
    return add

def addSInt(number):
    add = ""
    
    if number >= 2 or number == 0:
        add = "s"
        
    return add

def findFiles(inDir, recursive, extensionList, verbose):
    if recursive:
        print("\nScanning directory:\n%s\nrecursively..." % inDir)
    else:
        print("\nScanning directory:\n%s ..." % inDir)
    
    fileListC = [f for f in glob.glob(inDir + "**/**", recursive=True)] # complete list of files and directories
    
    if verbose:
        print("+++ Found %s item%s (including top directory)" % (len(fileListC), addS(fileListC)))
        
    if len(fileListC) <= 1:
        onError(8, "No items found")
        
    fileList = [] # find valid files and store them in list
    for item in fileListC:
        if os.path.isfile(item): # check if item is a file
            for extension in extensionList: 
                if os.path.splitext(item)[1].lower().strip(".") == extension.lower(): # check if match
                    fileList.append(item) # append to list
                    break
                
    if verbose:
        print("+++ Found %s valid file%s" % (len(fileList), addS(fileList)))
        for validFile in fileList:
            print("    %s" % validFile)  
            
    if len(fileList) == 0:
        onError(9, "No valid items found")      
    
    return fileList
    
def createPlaylist(files, outDir, outFilePath, absolutePath, append, verbose):
    linesWritten = 0    
        
    if append:
        if verbose:
            print("--- Opening file for appending text...")
        playlist = open(outFilePath, "a+")
    else:
        if verbose:
            print("--- Creating file...")
        playlist = open(outFilePath, "w+")
    
    if absolutePath:
        if verbose:
            print("--- Creating playlist with absolutePaths...")
            
    else:
        if verbose:
            print("--- Creating playlist...")
            
    for line in files: 
        linesWritten += 1
        if verbose:
            print("--- Writing line #%s ...\n%s" % (linesWritten, line))
        if absolutePath:
            playlist.write("%s\n" % line) # add line with absolute paths
        else:
            playlist.write("%s\n" % os.path.relpath(line, outDir)) # add line with relative paths
    
    if verbose:
        print("+++ %s line%s written\n--- Closing file..." % (linesWritten, addSInt(linesWritten)))
    else:
        print("\nWrote %s line%s" % (linesWritten, addSInt(linesWritten)))
            
    playlist.close()
    
    if append:
        lineCount = sum(1 for line in open(outFilePath))
        if verbose:
            print("+++ File now has %s line%s" % (lineCount, addSInt(lineCount)))
        else:
            print("\nFile now has %s line%s" % (lineCount, addSInt(lineCount)))
            
    
            
            
            
            
            
            
            
    
    
    