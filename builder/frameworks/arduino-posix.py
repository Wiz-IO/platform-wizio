# WizIO 2019 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO

# openssl ---> sudo apt-get install libssl-dev

import glob
import os
import re

import subprocess
from os.path import join
from shutil import copyfile
from SCons.Script import ARGUMENTS, DefaultEnvironment, Builder

def run_application(target, source, env):
    if env.get("PLATFORM") == "darwin": # Mac
        subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "Terminal", join(env.get("BUILD_DIR"), "program")])
    else:
        print("Where are we?", env.get("PLATFORM"))
        subprocess.call(['gnome-terminal', '-x', join(env.get("BUILD_DIR"), "program")])

def init_compiler(env):
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
        PROGSUFFIX="",
    )
    if env.get("PLATFORM") == "darwin":
        # Look for gcc
        gcc = None
        gcc_ver = 0
        for basedir in ["/usr/local/bin", "/opt/homebrew/bin"]:
            for candidate in glob.glob(join(basedir, "gcc*")):
                match = re.search("(?<=/gcc\-)\d*$", candidate)
                if match:
                    version = int(match.group())
                    if version > gcc_ver:
                        gcc = candidate
                        gcc_ver = version
        if gcc:
            print(f"Found GNU gcc: {gcc}")
        else:
            print(f"No GNU gcc found, please instal with brew install gcc")

        gcc_base = os.path.dirname(gcc)
        env.Replace(
            AR=join(gcc_base, f"gcc-ar-{gcc_ver}"),
            CC=join(gcc_base, f"gcc-{gcc_ver}"),
            CXX=join(gcc_base, f"g++-{gcc_ver}"),
        )

        # Add gtk4 dependencies. Will do nothing if gtk is not installed
        env.Append(
            CPPPATH = [ # -I
                subprocess.run(["pkg-config", "--cflags", "gtk4"],
                    capture_output=True).stdout.decode().strip()[2:].split(" -I")
            ],
            LIBS = [ # -l
             subprocess.run(["pkg-config", "--libs-only-l", "gtk4"],
                capture_output=True).stdout.decode().strip()[2:].split(" -l")
            ],
            LIBPATH = [ # -l
             subprocess.run(["pkg-config", "--libs-only-L", "gtk4"],
                capture_output=True).stdout.decode().strip()[2:].split(" -L")
            ],
        )

        # Add openssl dependencies. Will do nothing if openssl is not installed
        openssl_path = subprocess.run(["brew", "--prefix", "openssl@1.1"],
            capture_output=True).stdout.decode().strip()
        if openssl_path:
            env.Append(
                CPPPATH = [ join(openssl_path, "include") ],
                LIBPATH = [ join(openssl_path, "lib") ]
            )

def has_subdirs(basedir):
    # Checks if basedir has subdirs. This is necessary as ar on mac will fail
    # for an empty library
    if os.path.isdir(basedir):
        for f in os.listdir(basedir):
            if os.path.isdir(f):
                return True
    print(f"Skipping {basedir}, no subdirs")
    return False

def dev_init(env, platform):
    init_compiler(env)
    framework_dir = env.PioPlatform().get_package_dir("framework-wizio")
    variant = env.BoardConfig().get("build.variant")
    core = env.get("PLATFORM") # posix, windows or darwin
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
            "-Wno-pointer-sign",
        ],
        CXXFLAGS = [
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
        LINKFLAGS = ["-Wl,--gc-sections"] if (core != "darwin") else ["-W"],
        LIBPATH = [],
        LIBS = [
            "libcrypto", # openssl
            "libssl",
        ],
        LIBSOURCE_DIRS = [
            join(framework_dir, platform, "libraries"),
        ],
        UPLOADCMD = run_application
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
    if (core != "darwin") or has_subdirs(join(env.get("PROJECT_DIR"), "lib")):
        libs.append(
            env.BuildLibrary(
                join("$BUILD_DIR", "_custom_lib"),
                join("$PROJECT_DIR", "lib"),
        ))
    env.Append(LIBS = libs)
