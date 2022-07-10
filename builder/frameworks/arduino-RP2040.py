# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from common import *

def dev_init(env, platform):
    env.platform = platform
    env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-pico")
    env.libs = []
    dev_compiler(env, 'ARDUINO')
    dev_create_template(env)
    core = env.BoardConfig().get("build.core")
    variant= env.BoardConfig().get("build.variant")
    PLATFORM_DIR = join( env.framework_dir, platform )
    env.Append(
        CPPDEFINES = [ "ARDUINO=200" ],
        CPPPATH = [
            join(PLATFORM_DIR, platform),
            join(PLATFORM_DIR, "cores", core),
            join(PLATFORM_DIR, "variants", variant),
        ],
        LIBSOURCE_DIRS = [ join(PLATFORM_DIR, "libraries", core) ],
        LIBPATH        = [ join(PLATFORM_DIR, "libraries", core) ],
    )

    config_board(env)

    OBJ_DIR = join( "$BUILD_DIR", platform, "arduino" )
    env.BuildSources( join( OBJ_DIR, "arduino" ), join( PLATFORM_DIR, platform )  )
    env.BuildSources( join( OBJ_DIR, "core" ),    join( PLATFORM_DIR, "cores", core ) )
    env.BuildSources( join( OBJ_DIR, "variant" ), join( PLATFORM_DIR, "variants", variant )  )
    
    dev_finalize(env)

