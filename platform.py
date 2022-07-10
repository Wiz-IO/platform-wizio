# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from platformio.managers.platform import PlatformBase
import os, platform, copy
from os.path import join
from platform import system, machine

def get_system():
    sys_dir = system() +'_'+ machine()
    sys_dir = sys_dir.lower()
    if 'windows' in sys_dir: 
        sys_dir = 'windows'
    return sys_dir 

class WiziopicoPlatform(PlatformBase):
    def is_embedded(self):
        return True

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_dynamic_options(result)
        else:
            for key, value in result.items():
                result[key] = self._add_dynamic_options(result[key])
        return result
     
    def _add_dynamic_options(self, board):
        # upload protocols
        if not board.get("upload.protocols", []):
            board.manifest["upload"]["protocols"] = ["uf2"]
        if not board.get("upload.protocol", ""):
            board.manifest["upload"]["protocol"] = "uf2"
        # debug tools
        debug = board.manifest.get("debug", {})
        non_debug_protocols   = [ "uf2" ]
        supported_debug_tools = [ "cmsis-dap", "picoprobe", ]
        upload_protocol  = board.manifest.get("upload", {}).get("protocol")
        upload_protocols = board.manifest.get("upload", {}).get("protocols", [])
        if debug:
            upload_protocols.extend(supported_debug_tools)
        if upload_protocol and upload_protocol not in upload_protocols:
            upload_protocols.append(upload_protocol)
        board.manifest["upload"]["protocols"] = upload_protocols
        if "tools" not in debug:
            debug["tools"] = {}

        for link in upload_protocols:
            if link in non_debug_protocols or link in debug["tools"]: continue
            server_args = [
                "-s", "$PACKAGE_DIR/share/openocd/scripts",
                "-f", "interface/%s.cfg" % link,
                "-f", "target/%s" % debug.get("openocd_target")
            ]
            
            if link == "picoprobe":
                init_cmds = [ ] # use pio default settings
            else:
                init_cmds = [
                    "target extended-remote $DEBUG_PORT",
                    "define pio_reset_halt_target",
                    "end",
                    "define pio_reset_run_target",
                    "end"
                ]

            if link == 'picoprobe':
                debug["tools"][link] = {
                    "server": {
                        "package"    : "tool-pico-openocd",
                        "executable" : join(get_system(), "picoprobe"), # EXE
                        "arguments"  : server_args,
                    },
                    "init_cmds"      : init_cmds,
                    "onboard"        : link in debug.get("onboard_tools", []),
                    "default"        : link == debug.get("default_tool"),
                }                
            else: # CMSIS-DAP
                debug["tools"][link] = {
                    "server": {
                        "package"    : "tool-pico-openocd",
                        "executable" : join(get_system(), "openocd_rp2040"), # EXE
                        "arguments"  : server_args,
                    },
                    "init_cmds"      : init_cmds,
                    "onboard"        : link in debug.get("onboard_tools", []),
                    "default"        : link == debug.get("default_tool"),
                }

        board.manifest["debug"] = debug
        return board

    def configure_debug_options(self, initial_debug_options, ide_data):
        """
        Deprecated. Remove method when PlatformIO Core 5.2 is released
        """
        debug_options = copy.deepcopy(initial_debug_options)
        if "cmsis-dap" in debug_options["tool"]:
            debug_options["server"]["arguments"].extend( [
                    "-c", "adapter speed %s" % (initial_debug_options.get("speed") or "20000"),
                    "-c", "transport select swd"
                ]
            )
        return debug_options
