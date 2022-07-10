# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

import os
from os.path import join, normpath, basename
from shutil import copyfile
from colorama import Fore
from pico import *
from uf2conv import dev_uploader
from SCons.Script import DefaultEnvironment, Builder, ARGUMENTS

bynary_type_info = []

def do_copy(src, dst, name):
    if False == os.path.isfile( join(dst, name) ):
        copyfile( join(src, name), join(dst, name) )

def do_mkdir(path, name):
    dir = join(path, name)
    if False == os.path.isdir( dir ):
        try:
            os.mkdir(dir)
        except OSError:
            print ("[ERROR] Creation of the directory %s failed" % dir)
            exit(1)
    return dir

def ini_file(env):
    ini = join(env.subst("$PROJECT_DIR"), 'platformio.ini')
    f = open(ini, "r")
    txt = f.read()
    f.close()
    f = open(ini, "a+")
    if 'monitor_port'  not in txt: f.write("\n;monitor_port = SERIAL_PORT\n")
    if 'monitor_speed' not in txt: f.write(";monitor_speed = 115200\n")
    if 'build_flags'   not in txt: f.write("\n;build_flags = \n")
    if 'lib_deps'      not in txt: f.write("\n;lib_deps = \n")
    f.close()

def dev_create_template(env):
    ini_file(env)
    src = join(env.PioPlatform().get_package_dir("framework-wizio-pico"), "templates")
    dst = do_mkdir( env.subst("$PROJECT_DIR"), "include" )
    do_copy(src, dst, "tusb_config.h")

    if "freertos" in env.GetProjectOption("lib_deps", []) or "USE_FREERTOS" in env.get("CPPDEFINES"):
        do_copy(src, dst, "FreeRTOSConfig.h")

    if "VFS" in env.GetProjectOption("lib_deps", []) or "USE_VFS" in env.get("CPPDEFINES"):
        do_copy(src, dst, "vfs_config.h")

    if 'APPLICATION'== env.get("PROGNAME"):
        if "fatfs" in env.GetProjectOption("lib_deps", []):
            do_copy(src, dst, "ffconf.h")
        dst = do_mkdir( env.subst("$PROJECT_DIR"), join("include", "pico") )
        do_copy(src, dst, "config_autogen.h" )
        dst = join(env.subst("$PROJECT_DIR"), "src")
        if False == os.path.isfile( join(dst, "main.cpp") ):
            do_copy(src, dst, "main.c" )

    if 'BOOT-2'== env.get("PROGNAME"):
        dst = do_mkdir( env.subst("$PROJECT_DIR"), join("include", "pico") )
        do_copy(src, dst, "config_autogen.h" )

def dev_nano(env):
    enable_nano = env.BoardConfig().get("build.nano", "enable") # no <sys/lock>
    nano = []
    if enable_nano == "enable":
        nano = ["-specs=nano.specs", "-u", "_printf_float", "-u", "_scanf_float" ]
    if len(nano) > 0: print('  * SPECS        :', nano[0][7:])
    else:             print('  * SPECS        : default')
    return nano

def dev_compiler(env, application_name = 'APPLICATION'):
    env.sdk = env.BoardConfig().get("build.sdk", "SDK") # get/set default SDK
    env.variant = env.BoardConfig().get("build.variant", 'raspberry-pi-pico')
    print()
    print( Fore.BLUE + "%s RASPBERRYPI PI PICO RP2040 ( PICO - %s )" % (env.platform.upper(), env.sdk.upper()) )
    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-none-eabi-ar",
        AS="arm-none-eabi-as",
        CC="arm-none-eabi-gcc",
        GDB="arm-none-eabi-gdb",
        CXX="arm-none-eabi-g++",
        OBJCOPY="arm-none-eabi-objcopy",
        RANLIB="arm-none-eabi-ranlib",
        SIZETOOL="arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.boot2|\.rodata)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.ram_vector_table)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".elf",
        PROGNAME = application_name
    )
    cortex = ["-march=armv6-m", "-mcpu=cortex-m0plus", "-mthumb"]
    env.heap_size = env.BoardConfig().get("build.heap", "2048")
    optimization = env.BoardConfig().get("build.optimization", "-Os")
    stack_size = env.BoardConfig().get("build.stack", "2048")
    print('  * OPTIMIZATION :', optimization)
    if 'ARDUINO' == env.get("PROGNAME"):
        if "freertos" in env.GetProjectOption("lib_deps", []) or "USE_FREERTOS" in env.get("CPPDEFINES"):
            pass
        else:
            print('  * STACK        :', stack_size)
            print('  * HEAP         : maximum')
    else:
        print('  * STACK        :', stack_size)
        print('  * HEAP         :', env.heap_size)
    fix_old_new_stdio(env)
    env.Append(
        ASFLAGS=[ cortex, "-x", "assembler-with-cpp" ],
        CPPPATH = [
            join("$PROJECT_DIR", "src"),
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include"),
            join( env.framework_dir, "wizio", "pico"),
            join( env.framework_dir, "wizio", "newlib"),
            join( env.framework_dir, env.sdk, "include"),
            join( env.framework_dir, env.sdk, "cmsis", "include"), #
        ],
        CPPDEFINES = [
            "NDEBUG",
            "PICO_ON_DEVICE=1",
            "PICO_HEAP_SIZE="  + env.heap_size,
            "PICO_STACK_SIZE=" + stack_size,
        ],
        CCFLAGS = [
            cortex,
            optimization,
            "-fdata-sections",
            "-ffunction-sections",
            "-Wall",
            "-Wextra",
            "-Wfatal-errors",
            "-Wno-sign-compare",
            "-Wno-type-limits",
            "-Wno-unused-parameter",
            "-Wno-unused-function",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-unused-value",
            "-Wno-strict-aliasing",
            "-Wno-maybe-uninitialized"
        ],
        CFLAGS = [
            cortex,
            "-Wno-discarded-qualifiers",
            "-Wno-ignored-qualifiers",
            "-Wno-attributes", #
        ],
        CXXFLAGS = [
            "-fno-rtti",
            "-fno-exceptions",
            "-fno-threadsafe-statics",
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
        ],
        LINKFLAGS = [
            cortex,
            optimization,
            "-nostartfiles",
            "-Xlinker", "--gc-sections",
            "-Wl,--gc-sections",
            "--entry=_entry_point",
            dev_nano(env)
        ],
        LIBSOURCE_DIRS = [ join(env.framework_dir, "library"),  ],
        LIBPATH        = [ join(env.framework_dir, "library"), join("$PROJECT_DIR", "lib") ],
        LIBS           = ['m', 'gcc'],
        BUILDERS = dict(
            ElfToBin = Builder(
                action = env.VerboseAction(" ".join([
                    "$OBJCOPY", "-O",  "binary",
                    "$SOURCES", "$TARGET",
                ]), "Building $TARGET"),
                suffix = ".bin"
            )
        ),
        UPLOADCMD = dev_uploader
    )

def add_libraries(env): # is PIO LIB-s
    if "freertos" in env.GetProjectOption("lib_deps", []) or "USE_FREERTOS" in env.get("CPPDEFINES"):
        env.Append(  CPPPATH = [ join(join(env.framework_dir, "library", "freertos"), "include") ]  )
        print('  * RTOS         : FreeRTOS')
        if "USE_FREERTOS" not in env.get("CPPDEFINES"):
            env.Append(  CPPDEFINES = [ "USE_FREERTOS"] )

    if "cmsis-dap" in env.GetProjectOption("lib_deps", []):
        env.Append( CPPDEFINES = [ "DAP" ], )

def add_boot(env):
    boot = env.BoardConfig().get("build.boot", "w25q080") # get boot
    if "w25q080" != boot and "$PROJECT_DIR" in boot:
        boot = boot.replace('$PROJECT_DIR', env["PROJECT_DIR"]).replace("\\", "/")
    bynary_type_info.append(boot)
    env.BuildSources( join("$BUILD_DIR", env.platform, "wizio", "boot"), join(env.framework_dir, "boot", boot) )

def add_bynary_type(env):
    add_boot(env)
    bynary_type = env.BoardConfig().get("build.bynary_type", 'default')
    env.address = env.BoardConfig().get("build.address", "empty")
    linker      = env.BoardConfig().get("build.linker", "empty")
    if "empty" != linker and "$PROJECT_DIR" in linker:
        linker = linker.replace('$PROJECT_DIR', env["PROJECT_DIR"]).replace("\\", "/")
    if 'copy_to_ram' == bynary_type:
        if "empty" == env.address: env.address = '0x10000000'
        if "empty" == linker: linker = 'memmap_copy_to_ram.ld'
        env.Append(  CPPDEFINES = ['PICO_COPY_TO_RAM'] )
    elif 'no_flash' == bynary_type:
        if "empty" == env.address: env.address = '0x20000000'
        if "empty" == linker: linker = 'memmap_no_flash.ld'
        env.Append(  CPPDEFINES = ['PICO_NO_FLASH'] )
    elif 'blocked_ram' == bynary_type:
        print('TODO: blocked_ram is not supported yet')
        exit(0)
        if "empty" == env.address: env.address = ''
        if "empty" == linker: linker = ''
        env.Append( CPPDEFINES = ['PICO_USE_BLOCKED_RAM'] )
    else: #default
        if "empty" == env.address: env.address = '0x10000000'
        if "empty" == linker: linker = 'memmap_default.ld'
    env.Append( LDSCRIPT_PATH = join(env.framework_dir, env.sdk, "pico", "pico_standard_link", linker) )
    bynary_type_info.append(linker)
    bynary_type_info.append(env.address)
    print('  * BINARY TYPE  :' , bynary_type, bynary_type_info  )
    add_libraries(env)

def dev_finalize(env):
# WIZIO
    env.BuildSources( join("$BUILD_DIR", env.platform, "wizio"), join(env.framework_dir, "wizio") )
# SDK
    add_bynary_type(env)
    add_sdk(env)
    env.Append(LIBS = env.libs)
    print()

def config_board(env):
    src = join(env.PioPlatform().get_package_dir("framework-wizio-pico"), "templates")
    dst = do_mkdir( env.subst("$PROJECT_DIR"), "include" )

    ### default pico board
    if env.variant == "raspberry-pi-pico": 
        print("  * VARIANT      : PICO DEFAULT BOARD")
        return

    ### pico w board
    if env.variant == "raspberry-pi-pico-w":
        print("  * VARIANT      : PICO WIFI BOARD")

        do_copy(src, dst, "lwipopts.h")

        env.Append(
            CPPDEFINES = [ "PICO_W", ],
            CPPPATH = [
                join( env.framework_dir, env.sdk, "lib", "lwip", "src", "include" ),
                join( env.framework_dir, env.sdk, "lib", "cyw43-driver", "src" ),
                join( env.framework_dir, env.sdk, "lib", "cyw43-driver", "firmware" ),
            ],            
        )

        filter = [ "-<*>", "+<pico/pico_cyw43_arch>", "+<pico/pico_lwip>", ]
        NET_DIR = join( "$BUILD_DIR", env.platform, env.sdk, "network" )
        env.BuildSources( NET_DIR, join(env.framework_dir, env.sdk), src_filter = filter )

        LWIP_DIR = join( "$BUILD_DIR", env.platform, "lwip" )
        env.BuildSources( LWIP_DIR, join( env.framework_dir, env.sdk, "lib", "lwip", "src", "core" ),  )

        WIFI_DIR = join( "$BUILD_DIR", env.platform, "cyw43-driver" )
        env.BuildSources( WIFI_DIR, join( env.framework_dir, env.sdk, "lib", "cyw43-driver", "src" ),  )