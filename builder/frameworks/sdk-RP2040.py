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
    dev_compiler(env)
    dev_create_template(env)
    env.Append(
        CPPDEFINES = [ "BAREMETAL" ],
        CPPPATH    = [ join(env.framework_dir, env.sdk, "boards"), ]
    )
    config_board(env)
    dev_finalize(env)

