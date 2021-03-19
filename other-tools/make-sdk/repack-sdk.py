import os, shutil
from os.path import join, normpath, basename
from shutil import copyfile
from colorama import Fore
from subprocess import check_output, CalledProcessError, call, Popen, PIPE
from time import sleep

path            = os.path.dirname(__file__)
pico_sdk        = join(path, 'pico-sdk')
pico_sdk_src    = join(path, 'pico-sdk', 'src')
pico_sdk_lib    = join(path, 'pico-sdk', 'lib')
wizio_sdk       = join(path, "SDK")

def do_mkdir(path, name):
    dir = join(path, name)
    if False == os.path.isdir( dir ):
        try:
            os.mkdir(dir)
        except OSError:
            print ("[ERROR] Creation of the directory %s failed" % dir)
            exit(1)
        else:
            pass
    else:
        pass
    return dir

def sanitize_pico_sdk():
    if True == os.path.isdir( join(pico_sdk, 'docs') ):     shutil.rmtree(join(pico_sdk, 'docs'))
    if True == os.path.isdir( join(pico_sdk, 'cmake') ):    shutil.rmtree(join(pico_sdk, 'cmake'))
    if True == os.path.isdir( join(pico_sdk, 'external') ): shutil.rmtree(join(pico_sdk, 'external'))
    if True == os.path.isdir( join(pico_sdk, 'test') ):     shutil.rmtree(join(pico_sdk, 'test'))
    if True == os.path.isdir( join(pico_sdk_src, 'host') ): shutil.rmtree(join(pico_sdk_src, 'host'))
    for root, dirs, files in os.walk(path):
        for f in files:
            if '.txt' in f or '.cmake' in f or '.md' in f:
                file = join(root, f)
                if os.path.exists( file ):
                    print( file )
                    os.remove( file )

def sanitize_sdk():
    for root, dirs, files in os.walk(pico_sdk):
        if not os.listdir(root) :
            shutil.rmtree(root)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
                pass
            except: pass
        else:
            try:
                shutil.copy2(s, d)    
                pass            
            except: pass

def copy_hardware(Dst):
    for root, dirs, files in os.walk(pico_sdk_src):
        src = os.path.basename(root)
        if 'hardware_' in src:
            for f in files:
                if '.c' in f or '.S' in f:
                    if False == os.path.isfile( join(Dst, f) ): 
                        copyfile( join(root, f), join(Dst, f) )

def copy_pico(dst):
    for root, dirs, files in os.walk(pico_sdk_src):
        src = os.path.basename(root)
        if 'include'     in root: continue
        if 'asminclude'  in root: continue
        if 'boot_stage2' in root: continue
        if 'hardware_'   in root: continue
        if 'pico_'   not in root: continue
        name = root[root.index('pico_'):]
        do_mkdir(join(wizio_sdk, dst), name)
        for f in files:
            if '.c' in f or '.S' in f or '.ld' in f:
                file = join(dst, name, f)
                if False == os.path.isfile( file ): 
                    copyfile( join(root, f), file )

def copy_include(dst):
    for root, dirs, files in os.walk(pico_sdk_src):
        src = os.path.basename(root)
        if 'asminclude'  in root: continue
        if 'boot_stage2' in root: continue
        if 'boards'      in root: continue
        if 'include' not in root: continue
        name = root[root.index('include') + 8:]
        do_mkdir( join(wizio_sdk, dst), name )
        for f in files:
            if '.h' in f or '.S' in f:
                file = join(dst, name, f)
                if False == os.path.isfile( file ): 
                    copyfile( join(root, f), file ) 

def main():
    global path, sdk
    if False == os.path.isdir( pico_sdk ): print('[ERROR] "pico-sdk" not exist:', pico_sdk)
    sanitize_pico_sdk()

    do_mkdir(path, "SDK")
    do_mkdir(wizio_sdk, 'boards')
    do_mkdir(wizio_sdk, 'boot_stage2')
    do_mkdir(wizio_sdk, 'hardware')
    do_mkdir(wizio_sdk, 'include')
    do_mkdir(wizio_sdk, 'pico')
    do_mkdir(wizio_sdk, 'lib')
    do_mkdir(wizio_sdk, join('lib', 'tinyusb'))
    do_mkdir(wizio_sdk, join('lib', 'tinyusb', 'src'))
    do_mkdir(wizio_sdk, join('lib', 'tinyusb', 'src', 'portable'))

    copytree( join(pico_sdk_src, 'rp2_common', 'boot_stage2'), join(wizio_sdk, 'boot_stage2') )
    copytree( join(pico_sdk_src, 'boards', 'include'), join(wizio_sdk, 'boards') )
    copy_hardware( join(wizio_sdk, 'hardware') )
    copy_pico    ( join(wizio_sdk, 'pico') )
    copy_include ( join(wizio_sdk, 'include') )

    copytree( join(pico_sdk_lib, 'tinyusb', 'src'), join(wizio_sdk, 'lib', 'tinyusb', 'src') )   
    copytree( join(pico_sdk_lib, 'tinyusb', 'src', 'portable', 'raspberrypi'), join(wizio_sdk, 'lib', 'tinyusb', 'src', 'portable', 'raspberrypi') ) 

    pass

if __name__ == "__main__":
    print('----- BEGIN -----')
    main()
    print('------ END ------')