# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from __future__ import print_function
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore
from wpioasm import dev_pioasm # https://github.com/Wiz-IO/wizio-pico/issues/98#issuecomment-1128747885

env = DefaultEnvironment()
print( '<<<<<<<<<<<< ' + env.BoardConfig().get("name").upper() + " 2021 Georgi Angelov >>>>>>>>>>>>" )

dev_pioasm(env)

elf = env.BuildProgram()
src = env.ElfToBin( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg = env.Alias( "buildprog", src, [ env.VerboseAction("", "DONE") ] )
AlwaysBuild( prg )

upload = env.Alias("upload", prg, [ 
    env.VerboseAction("$UPLOADCMD", "Uploading..."),
    env.VerboseAction("", ""),
])
AlwaysBuild( upload )    

debug_tool = env.GetProjectOption("debug_tool")
if None == debug_tool:
    Default( prg )
else:   
    if 'cmsis-dap' in debug_tool:
        Default( upload )
    else:
        Default( prg )

