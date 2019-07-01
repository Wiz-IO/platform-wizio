# WizIO 2019 Georgi Angelov
# http://www.wizio.eu/
# https://github.com/Wiz-IO

import os
from os.path import join
from shutil import copyfile
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder

def dev_uploader(target, source, env):   
    FILES_DIR = join(env.PioPlatform().get_package_dir("framework-wizio"), "arduino", "cores", env.BoardConfig().get("build.core"),"files")
    BUILD_DIR = env.get("BUILD_DIR")
    
    #### copy dll-s if not exist
    DST = join(BUILD_DIR, "libcrypto-1_1.dll")
    if False == os.path.isfile(DST):
        copyfile(join(FILES_DIR, "libcrypto-1_1.dll"), DST)

    DST = join(BUILD_DIR, "libssl-1_1.dll")    
    if False == os.path.isfile(DST):
        copyfile(join(FILES_DIR, "libssl-1_1.dll"), DST)
    
    ### run app
    exe = join(BUILD_DIR, "program.exe")
    os.startfile(exe)
    return 

def dev_nope(target, source, env):
    return

def dev_compiler(env):
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="ar",
        AS="as",
        CC="gcc",
        GDB="gdb",
        CXX="g++",
        OBJCOPY="objcopy",
        RANLIB="ranlib",
        SIZETOOL="size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.bootloader)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".exe",  
    )
    env.Append(UPLOAD_PORT='RUN APPLICATION') #upload_port = "must exist variable"

def dev_init(env, platform):    
    dev_compiler(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-wizio")
    PC = env.get("PLATFORM") # win32
    if PC.startswith("win"):
        core = "windows"    
    variant = env.BoardConfig().get("build.variant")   
    visual = env.BoardConfig().get("build.visual", "0")
    env.Append(
       CPPDEFINES = [ # -D 
            "{}=200".format(platform.upper()), 
            "CORE_" + core.upper().replace("-", "_"), 
        ],        
        CPPPATH = [ # -I
            join(framework_dir,  platform, platform),
            join(framework_dir,  platform, "cores", core),
            join(framework_dir,  platform, "variants", variant),      
            join("$PROJECT_DIR"),         
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include")       
        ],        
        CFLAGS = [      
            #"-std=c11",  
            "-Wno-pointer-sign",      
        ],
        CXXFLAGS = [   
            #"-std=c++11",                             
            "-fno-rtti",
            "-fno-exceptions", 
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
            "-fno-threadsafe-statics",
        ],    
        CCFLAGS = [
            "-Os", "-g",                                
            "-fdata-sections",      
            "-ffunction-sections",
            "-fno-strict-aliasing",
            #"-fsingle-precision-constant",             
            "-Wall", 
            "-Wstrict-prototypes", 
            "-Wp,-w",       
               
        ],        
        LINKFLAGS = [                                                        
            #"-static-libgcc", 
            #"-static-libstdc++",                     
        ],    
        LIBPATH = [ 
            #lib_dir, 
            join(framework_dir, platform, "cores", core, "files")
        ],      
        #LDSCRIPT_PATH = linker, 
        LIBS = [ 
            "m", "gcc", 
            "libws2_32",                 
            "libcrypto",
            "libssl",
            "winmm" # timeGetTime() millis()  
        ],     
        LIBSOURCE_DIRS=[ 
            join(framework_dir, platform, "libraries"),             
        ],   
                
        BUILDERS = dict(
            ElfToBin   = Builder( action = env.VerboseAction(dev_nope, "MAKE DAT"), suffix = ".dat" ), # NOT USED   
            MakeHeader = Builder( action = env.VerboseAction(dev_nope, "MAKE BIN"), suffix = ".bin" )  # NOT USED     
        ), 
        
        UPLOADCMD = dev_uploader # RUN APP
    )

    libs = []
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_" + platform),
            join(framework_dir, platform, platform),
    ))    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_core"),
            join(framework_dir, platform, "cores", core),
    ))    
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_variant"),
            join(framework_dir, platform, "variants", variant),
    ))            
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom_lib"), 
            join("$PROJECT_DIR", "lib"),                       
    ))      
    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "_custom_config"), 
            join("$PROJECT_DIR", "config"),                       
    ))      
    env.Append(LIBS = libs)   

    # ENABLE VISUAL
    if PC.startswith("win"): 
        if visual == "1" or visual == "2":
            env.Append(LIBS="libcomctl32")
            env.Append(LIBS="libgdi32")
            env.Append(CPPDEFINES="WIN_EMU")
        if visual == "1":
            env.Append(LINKFLAGS="-Wl,--subsystem,windows")     