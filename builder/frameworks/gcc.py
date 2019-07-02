# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO

import os
import subprocess
from os.path import join
from shutil import copyfile
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder

def create_main(env):
    main = join(env.subst("$PROJECT_DIR"), "src", "main.cpp")
    if False == os.path.isfile(main):
        file = open(main, "w")  
        file.write('#include <stdio.h>\n\nint main() {\n\tprintf("GCC Hello World");\n\twhile (1) {}\n\treturn 0;\n}') 
        file.close() 

def run_application(target, source, env):  
    BUILD_DIR = env.get("BUILD_DIR")  
    PC = env.get("PLATFORM") 
    if PC.startswith("win"): 
        os.startfile( join(BUILD_DIR, "program") )
        return
    if PC.startswith("posix"):
        subprocess.call(['gnome-terminal', '-x', join(BUILD_DIR, "program")])

def init_compiler(env):
    env.Replace(
        BUILD_DIR   = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR          = "ar",
        AS          = "as",
        CC          = "gcc",
        GDB         = "gdb",
        CXX         = "g++",
        OBJCOPY     = "objcopy",
        RANLIB      = "ranlib",
        SIZETOOL    = "size",
        ARFLAGS     = ["rc"],
        #SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
        #SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        LIBSOURCE_DIRS=[], # remove arduino libraries
    )

def dev_init(env, platform):
    create_main(env)
    init_compiler(env)
    env.Append(
       CPPDEFINES = [],     # -D       
        CPPPATH = [         # -I     
            join("$PROJECT_DIR"),         
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")       
        ],        
        #CFLAGS = [],
        #CXXFLAGS = [],    
        #CCFLAGS = [],        
        #LINKFLAGS = [],    
        #LIBPATH = [],      
        #LIBS = [],     
        #LIBSOURCE_DIRS=[], 
        UPLOADCMD = run_application
    )
    libs = []         
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom_lib"), 
            join("$PROJECT_DIR", "lib"),                       
    ))          
    env.Append(LIBS = libs)  

    # Add some default libraries    
    pc = env.get("PLATFORM") 
    if pc.startswith("win"): 
        env.Replace( PROGSUFFIX=".exe" )    
        env.Append(LIBS="libws2_32")
        env.Append(LIBS="winmm")     
    elif pc.startswith("posix"):  
        #OPENSSL sudo apt-get install libssl-dev  
        env.Append(LIBS="libcrypto")
        env.Append(LIBS="libssl")             

######################################################
#print env.Dump()
dev_init(DefaultEnvironment(), "gcc")    
######################################################