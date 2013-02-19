#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# (c) Roberto Gambuzzi
# Creato:          19/02/2013 15:58:58
# Ultima Modifica: 19/02/2013 15:59:08
# 
# v 0.0.1.0
# 
# file: C:\workspaces\pymodman\modman.py
# auth: Roberto Gambuzzi <gambuzzi@gmail.com>
# desc: 
# 
# $Id: modman.py 19/02/2013 15:59:08 Roberto $
# --------------
import sys
import os

class Quiet:
    def __init__(self):
        return
    def write(self,s):
        return

def init(options, args):
    str_message = ''
    #recupera cartella
    if args:
        basedir = args[0]
    else:
        basedir = None
    #controlla sia una cartella
    if basedir and not os.path.isdir(basedir):
        print basedir + " is not a directory."
        return 1
    #prova a creare la certella modman
    try:
        os.mkdir('.modman')
    except:
        print "Could not create .modman directory"
        return 1
    #si segna la basedir
    if basedir:
        print >> open(os.path.join('.modman', '.basedir'), 'w'), basedir
        str_message = "with basedir at '"+basedir+"'"
    print "Initialized Module Manager at '"+os.getcwd()+"' "+str_message
    return 0
    

def main(options, args):
    if options.debug: print(options, args)
    switch = {
        'init':init,
    }
    if args[0] in switch:
        return switch[args[0]](options, args[1:])
    return 0

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(
        usage="%prog <command> [--force]",
        version="%prog 0.0.1.0"
    )

    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="print extra messages to stdout")

    (options, args) = parser.parse_args()
    if not options.verbose: sys.stdout = Quiet()
    sys.exit(main(options, args))
