#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt

# import modules from file modules.py
from modules import onError, usage

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'vh',
                                 ['verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
verbose = False
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
        
