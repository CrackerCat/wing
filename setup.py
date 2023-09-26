#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief:  ......
# @date:   2023.09.10 14:40:50

import os
import sys
import shutil
os.system("") # Unable to explain this, just for Windows cmd color print

from utils.utils_cmn import CmnUtils
from utils.utils_logger import LoggerUtils
from utils.utils_import import ImportUtils

g_this_file = os.path.realpath(sys.argv[0])
g_this_path = os.path.dirname(g_this_file)
sys.path.append(os.path.dirname(g_this_path))

g_wing_path = ImportUtils.initEnv()
g_bin_path = os.path.expanduser("~") + '/bin' # such as: /Users/${username}/bin
# --------------------------------------------------------------------------------------------------------------------------


def createPath(path):
    if os.path.isdir(path): return
    os.makedirs(path)
    if os.path.isdir(path): return
    LoggerUtils.e('No access permissions for ' + path)


def doClean():
    LoggerUtils.println('rm files ...')
    try:
        ppath = os.path.dirname(g_wing_path)
        if os.path.isdir(ppath): shutil.rmtree(ppath)
        LoggerUtils.println('rm bin')
        if CmnUtils.isOsWindows():
            f = g_bin_path + os.sep + 'wing.py'
            if os.path.isfile(f): os.remove(f)
            f = g_bin_path + os.sep + 'wing.bat'
            if os.path.isfile(f): os.remove(f)
        else:
            f = g_bin_path + os.sep + 'wing'
            if os.path.isfile(f): os.remove(f)
    except Exception as e:
        print(e)


def printInfo():
    print('         ' + setup_config['name'])
    print('version: ' + setup_config['version'])
    print(' author: ' + setup_config['author'])
    print('  email: ' + setup_config['author_email'])
    print('         ' + setup_config['description'])


def doInstall():
    createPath(g_bin_path)
    LoggerUtils.println('copy files ...')
    try:
        if os.path.isdir(g_wing_path): shutil.rmtree(g_wing_path)
        shutil.copytree(g_this_path, g_wing_path)
        LoggerUtils.println('copy bin')
        if CmnUtils.isOsWindows():
            shutil.copyfile(g_this_path + os.sep + 'wing.py', g_bin_path + os.sep + 'wing.py')
            shutil.copyfile(g_this_path + os.sep + 'wing.bat', g_bin_path + os.sep + 'wing.bat')
        else:
            shutil.copyfile(g_this_path + os.sep + 'wing.py', g_bin_path + os.sep + 'wing')
            CmnUtils.doCmd('chmod a+x %s ' % (g_bin_path + os.sep + 'wing'))

        printInfo()
        LoggerUtils.light(' success.')
        return
    except Exception as e:
        print(e)
    LoggerUtils.e('Install failed, rolling back ...')
    doClean()


def doUninstall():
    doClean()
    print('done.')


setup_config = {
    'name'          :'wing',
    'version'       :'0.9.2',
    'author'        :'iofomo',
    'author_email'  :'rd-share@iofomo.com',
    'description'   :'Develop tools'
}


def run():
    if 1 < len(sys.argv):
        if sys.argv[1] == 'install':
            doInstall()
            return
        if sys.argv[1] == 'uninstall':
            doUninstall()
            return
    print(
        '''
            The most similar command is 
                install
                uninstall 
        '''
    )


if __name__ == "__main__":
    run()