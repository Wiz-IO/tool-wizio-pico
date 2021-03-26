
import os, shutil
from os.path import join, normpath, basename

once = ""
cnt = 0

def add_wrap(wrap, file_name):
    global cnt, once
    if once != file_name:
        once = file_name
        print( file_name )
    cnt += 1
    print('            "-Wl,-wrap,' + wrap + '",')

def wrap(file_name, name):
    global once
    once = ""
    F = open(file_name, 'r')
    Lines = F.readlines()
    D = os.path.dirname(file_name)
    for line in Lines: # pico_wrap_function(${TARGET} cos)
        if 'pico_wrap_function' in line:
            line = line.replace('${TARGET}', 'TARGET').strip()
            line = line.replace('pico_wrap_function', '')
            line = line.replace('(', '')
            line = line.replace(')', '')
            w = line.split()
            add_wrap( w[1], file_name )

    F.close()  
    once = ""

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if 'CMakeLists.txt' not in f: continue
            wrap( join(root, f), f )

def main():
    list_files("D:/DOWNLOAD/PICO/pico-sdk-1.1.0/pico-sdk-1.1.0/src") # path to sdk
    print("COUNT", cnt)
    pass

if __name__ == "__main__":
    main()            