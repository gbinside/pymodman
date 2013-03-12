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
import platform
import sys
import re
import os

class Quiet:
    def __init__(self):
        return
    def write(self,s):
        return

def require_wc(module, folder = '.modman'):
    if not os.path.exists(os.path.join(folder, module)):
        print "ERROR: %s has not been checked out." % module
        return 1
    if not os.path.exists(os.path.join(folder, module, 'modman')):
        print 'ERROR: %s does not contain a "modman" module description file.' % module
        return 1
    return 0

def symlink(src, dst):
    if platform.system() == 'Windows':
        if os.path.isdir(src):
            retcode = os.system('mklink /J "%s" "%s"' % (dst, src ))
        else:
            retcode = os.system('mklink /H "%s" "%s"' % (dst, src ))
        if retcode:
            print "There was an error"
            if options.debug: print "retcode", retcode
            return retcode
    else: #i hope is linux
        os.symlink(src, dst)
    return 0

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

def update(options, args):
    predir = os.getcwd()
    #todo implementare basedir
    using_basedir = ''
    module = args[0]
    os.chdir ( os.path.join ( '.modman', module ) )
    s_args = ''.join(args)
    retcode = os.system('git pull')
    if retcode:
        print "There was an error"
        if options.debug: print "retcode", retcode
        return retcode

    print "Successfully updated module '"+module+"' "+using_basedir
    os.chdir(predir)

    return main(options, ['deploy',module])

def clone(options, args):
    predir = os.getcwd()
    #todo implementare basedir
    using_basedir = ''
    os.chdir ( '.modman' )
    s_args = ''.join(args)
    retcode = os.system('git clone' + s_args)
    if retcode:
        print "There was an error"
        if options.debug: print "retcode", retcode
        return retcode
    module = ''.join(re.findall(r'.*?/([^/.]*)', s_args, re.I))

    print "Successfully cloned new module '"+module+"' "+using_basedir
    os.chdir(predir)

    return main(options, ['deploy',module])

def deploy(options, args):
    module = args[0]
    base_path = os.getcwd() #todo implementare basedir
    retcode = require_wc(module)
    if retcode: return retcode
    modman_file = os.path.join('.modman', module, 'modman')
    for line in open(modman_file):
        if options.debug: print 'line ==>', line,
        line = line.strip('\n\r ')
        da, a = re.split('\s+', line, maxsplit=1)
        da = da.replace('/', os.sep)
        a  =  a.replace('/', os.sep)
        if options.debug: print 'from ==>', da
        if options.debug: print ' to  ==>', a
        try:
            os.makedirs ( os.path.join(base_path, os.path.dirname(a.strip(os.sep)) ) )
        except:
            pass
        if options.debug: print ( os.path.join('.modman', module, da) , os.path.join(base_path,a) )
        symlink( os.path.join('.modman', module, da) , os.path.join(base_path,a) )
    return 0

def main(options, args):
    if options.debug: print(options, args)
    switch = {
        'init':init,
        'clone':clone,
        'update':update,
        'deploy':deploy,
    }
    if args and args[0] in switch:
        return switch[args[0]](options, args[1:])
    else:
        print "Use -h for help"
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
