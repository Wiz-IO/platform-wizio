# WizIO 2021 Georgi Angelov
#   http://www.wizio.eu/
#   https://github.com/Wiz-IO/wizio-pico

from os.path import join
from SCons.Script import DefaultEnvironment, Builder
from platformio.builder.tools.piolib import PlatformIOLibBuilder


# SDK >= 1.2 : LIB_PICO_STDIO_FOO
# SDK  < 1.2 : PICO_STDIO_FOO
# this add both keys...
def fix_old_new_stdio(env):
    if "PICO_STDIO_UART" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "LIB_PICO_STDIO_UART"] )
    if "LIB_PICO_STDIO_UART" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "PICO_STDIO_UART"] )

    if "PICO_STDIO_USB" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "LIB_PICO_STDIO_USB"] )
    if "LIB_PICO_STDIO_USB" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "PICO_STDIO_USB"] )

    if "PICO_STDIO_SEMIHOSTING" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "LIB_PICO_STDIO_SEMIHOSTING"] )
    if "LIB_PICO_STDIO_SEMIHOSTING" in env.get("CPPDEFINES"):
        env.Append( CPPDEFINES = [ "PICO_STDIO_SEMIHOSTING"] )


def add_ops(env):
    tab = '  *'
    OBJ_DIR = join( "$BUILD_DIR", env.platform, env.sdk, "pico" )
    LIB_DIR  = join( env.framework_dir, env.sdk, "pico" )
    if "PICO_DOUBLE_SUPPORT_ROM_V1" in env.get("CPPDEFINES"):
        print(tab, 'PICO_DOUBLE_SUPPORT_ROM_V1')
        env.BuildSources( join(OBJ_DIR, "pico_double"), join(LIB_DIR, "pico_double") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,__aeabi_dadd",
            "-Wl,-wrap,__aeabi_ddiv",
            "-Wl,-wrap,__aeabi_dmul",
            "-Wl,-wrap,__aeabi_drsub",
            "-Wl,-wrap,__aeabi_dsub",
            "-Wl,-wrap,__aeabi_cdcmpeq",
            "-Wl,-wrap,__aeabi_cdrcmple",
            "-Wl,-wrap,__aeabi_cdcmple",
            "-Wl,-wrap,__aeabi_dcmpeq",
            "-Wl,-wrap,__aeabi_dcmplt",
            "-Wl,-wrap,__aeabi_dcmple",
            "-Wl,-wrap,__aeabi_dcmpge",
            "-Wl,-wrap,__aeabi_dcmpgt",
            "-Wl,-wrap,__aeabi_dcmpun",
            "-Wl,-wrap,__aeabi_i2d",
            "-Wl,-wrap,__aeabi_l2d",
            "-Wl,-wrap,__aeabi_ui2d",
            "-Wl,-wrap,__aeabi_ul2d",
            "-Wl,-wrap,__aeabi_d2iz",
            "-Wl,-wrap,__aeabi_d2lz",
            "-Wl,-wrap,__aeabi_d2uiz",
            "-Wl,-wrap,__aeabi_d2ulz",
            "-Wl,-wrap,__aeabi_d2f",
            "-Wl,-wrap,sqrt",
            "-Wl,-wrap,cos",
            "-Wl,-wrap,sin",
            "-Wl,-wrap,tan",
            "-Wl,-wrap,atan2",
            "-Wl,-wrap,exp",
            "-Wl,-wrap,log",
            "-Wl,-wrap,ldexp",
            "-Wl,-wrap,copysign",
            "-Wl,-wrap,trunc",
            "-Wl,-wrap,floor",
            "-Wl,-wrap,ceil",
            "-Wl,-wrap,round",
            "-Wl,-wrap,sincos",
            "-Wl,-wrap,asin",
            "-Wl,-wrap,acos",
            "-Wl,-wrap,atan",
            "-Wl,-wrap,sinh",
            "-Wl,-wrap,cosh",
            "-Wl,-wrap,tanh",
            "-Wl,-wrap,asinh",
            "-Wl,-wrap,acosh",
            "-Wl,-wrap,atanh",
            "-Wl,-wrap,exp2",
            "-Wl,-wrap,log2",
            "-Wl,-wrap,exp10",
            "-Wl,-wrap,log10",
            "-Wl,-wrap,pow",
            "-Wl,-wrap,powint",
            "-Wl,-wrap,hypot",
            "-Wl,-wrap,cbrt",
            "-Wl,-wrap,fmod",
            "-Wl,-wrap,drem",
            "-Wl,-wrap,remainder",
            "-Wl,-wrap,remquo",
            "-Wl,-wrap,expm1",
            "-Wl,-wrap,log1p",
            "-Wl,-wrap,fma",
        ])

    if "PICO_FLOAT_SUPPORT_ROM_V1" in env.get("CPPDEFINES"):
        print(tab, 'PICO_FLOAT_SUPPORT_ROM_V1')
        env.BuildSources( join(OBJ_DIR, "pico_float"), join(LIB_DIR, "pico_float") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,__aeabi_fadd",
            "-Wl,-wrap,__aeabi_fdiv",
            "-Wl,-wrap,__aeabi_fmul",
            "-Wl,-wrap,__aeabi_frsub",
            "-Wl,-wrap,__aeabi_fsub",
            "-Wl,-wrap,__aeabi_cfcmpeq",
            "-Wl,-wrap,__aeabi_cfrcmple",
            "-Wl,-wrap,__aeabi_cfcmple",
            "-Wl,-wrap,__aeabi_fcmpeq",
            "-Wl,-wrap,__aeabi_fcmplt",
            "-Wl,-wrap,__aeabi_fcmple",
            "-Wl,-wrap,__aeabi_fcmpge",
            "-Wl,-wrap,__aeabi_fcmpgt",
            "-Wl,-wrap,__aeabi_fcmpun",
            "-Wl,-wrap,__aeabi_i2f",
            "-Wl,-wrap,__aeabi_l2f",
            "-Wl,-wrap,__aeabi_ui2f",
            "-Wl,-wrap,__aeabi_ul2f",
            "-Wl,-wrap,__aeabi_f2iz",
            "-Wl,-wrap,__aeabi_f2lz",
            "-Wl,-wrap,__aeabi_f2uiz",
            "-Wl,-wrap,__aeabi_f2ulz",
            "-Wl,-wrap,__aeabi_f2d",
            "-Wl,-wrap,sqrtf",
            "-Wl,-wrap,cosf",
            "-Wl,-wrap,sinf",
            "-Wl,-wrap,tanf",
            "-Wl,-wrap,atan2f",
            "-Wl,-wrap,expf",
            "-Wl,-wrap,logf",
            "-Wl,-wrap,ldexpf",
            "-Wl,-wrap,copysignf",
            "-Wl,-wrap,truncf",
            "-Wl,-wrap,floorf",
            "-Wl,-wrap,ceilf",
            "-Wl,-wrap,roundf",
            "-Wl,-wrap,sincosf",
            "-Wl,-wrap,asinf",
            "-Wl,-wrap,acosf",
            "-Wl,-wrap,atanf",
            "-Wl,-wrap,sinhf",
            "-Wl,-wrap,coshf",
            "-Wl,-wrap,tanhf",
            "-Wl,-wrap,asinhf",
            "-Wl,-wrap,acoshf",
            "-Wl,-wrap,atanhf",
            "-Wl,-wrap,exp2f",
            "-Wl,-wrap,log2f",
            "-Wl,-wrap,exp10f",
            "-Wl,-wrap,log10f",
            "-Wl,-wrap,powf",
            "-Wl,-wrap,powintf",
            "-Wl,-wrap,hypotf",
            "-Wl,-wrap,cbrtf",
            "-Wl,-wrap,fmodf",
            "-Wl,-wrap,dremf",
            "-Wl,-wrap,remainderf",
            "-Wl,-wrap,remquof",
            "-Wl,-wrap,expm1f",
            "-Wl,-wrap,log1pf",
            "-Wl,-wrap,fmaf",
        ])

    if "PICO_DIVIDER_HARDWARE" in env.get("CPPDEFINES"):
        print(tab, 'PICO_DIVIDER_HARDWARE')
        env.BuildSources( join(OBJ_DIR, "pico_divider"), join(LIB_DIR, "pico_divider") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,__aeabi_idiv",
            "-Wl,-wrap,__aeabi_idivmod",
            "-Wl,-wrap,__aeabi_ldivmod",
            "-Wl,-wrap,__aeabi_uidiv",
            "-Wl,-wrap,__aeabi_uidivmod",
            "-Wl,-wrap,__aeabi_uldivmod",
        ])

    if "PICO_INT64_OPS_PICO" in env.get("CPPDEFINES"):
        print(tab, 'PICO_INT64_OPS_PICO')
        env.BuildSources( join(OBJ_DIR, "pico_int64_ops"), join(LIB_DIR, "pico_int64_ops") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,wrapper_func __aeabi_lmul",
        ])

    if "PICO_BIT_OPS_PICO" in env.get("CPPDEFINES"):
        print(tab, 'PICO_BIT_OPS_PICO')
        env.BuildSources( join(OBJ_DIR, "pico_bit_ops"), join(LIB_DIR, "pico_bit_ops") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,__clzsi2",
            "-Wl,-wrap,__clzsi2",
            "-Wl,-wrap,__clzdi2",
            "-Wl,-wrap,__ctzsi2",
            "-Wl,-wrap,__ctzdi2",
            "-Wl,-wrap,__popcountsi2",
            "-Wl,-wrap,__popcountdi2",
            #"-Wl,-wrap,__clz",
            #"-Wl,-wrap,__clzl",
            #"-Wl,-wrap,__clzsi2",
            #"-Wl,-wrap,__clzll",
        ])

    if "PICO_MEM_OPS_PICO" in env.get("CPPDEFINES"):
        print(tab, 'PICO_MEM_OPS_PICO')
        env.BuildSources( join(OBJ_DIR, "pico_mem_ops"), join(LIB_DIR, "pico_mem_ops") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,memcpy",
            "-Wl,-wrap,memset",
            "-Wl,-wrap,__aeabi_memcpy",
            "-Wl,-wrap,__aeabi_memset",
            "-Wl,-wrap,__aeabi_memcpy4",
            "-Wl,-wrap,__aeabi_memset4",
            "-Wl,-wrap,__aeabi_memcpy8",
            "-Wl,-wrap,__aeabi_memset8",
        ])

    if 'ARDUINO' == env.get("PROGNAME"):
        return ########################################################################################

    if "PICO_PRINTF_PICO" in env.get("CPPDEFINES"):
        print(tab, 'PICO_PRINTF_PICO')
        env.BuildSources( join(OBJ_DIR, "pico_printf"), join(LIB_DIR, "pico_printf") )
        env.Append( LINKFLAGS = [
            "-Wl,-wrap,sprintf",
            "-Wl,-wrap,snprintf",
            "-Wl,-wrap,vsnprintf",

            "-Wl,-wrap,printf",
            "-Wl,-wrap,vprintf",
            "-Wl,-wrap,puts",
            "-Wl,-wrap,putchar",
        ])

    if "PICO_STDIO_USB" in env.get("CPPDEFINES") or "PICO_STDIO_UART" in env.get("CPPDEFINES") or "PICO_STDIO_SEMIHOSTING" in env.get("CPPDEFINES"):     
        env.BuildSources( join(OBJ_DIR, "pico_stdio"), join(LIB_DIR, "pico_stdio") )

    if "PICO_STDIO_USB" in env.get("CPPDEFINES"):
        print(tab, 'STDIO        : USB')
        env.BuildSources( join(OBJ_DIR, "pico_stdio_usb"), join(LIB_DIR, "pico_stdio_usb") )        

    if "PICO_STDIO_UART" in env.get("CPPDEFINES"):
        print(tab, 'STDIO        : UART')
        env.BuildSources( join(OBJ_DIR, "pico_stdio_uart"), join(LIB_DIR, "pico_stdio_uart") )

    if "PICO_STDIO_SEMIHOSTING" in env.get("CPPDEFINES"):
        print(tab, 'STDIO        : SEMIHOSTING')
        env.BuildSources( join(OBJ_DIR, "pico_stdio_semihosting"), join(LIB_DIR, "pico_stdio_semihosting") )

    env.Append( LINKFLAGS = [
        "-Wl,-wrap,malloc",
        "-Wl,-wrap,calloc",
        "-Wl,-wrap,free",
    ])


def add_tinyusb(env):
    OBJ_DIR = join( "$BUILD_DIR", env.platform, env.sdk, "pico", "usb" )
    USB_DIR = join( env.framework_dir, env.sdk, "lib", "tinyusb", "src" )
    for define in env.get("CPPDEFINES"):
        if "USB" in define:
            env.Append( CPPDEFINES = [ "CFG_TUSB_MCU=OPT_MCU_RP2040", "CFG_TUSB_OS=OPT_OS_PICO" ], CPPPATH = [ USB_DIR ]  )
            if "PICO_USB_HOST" in define: 
                #[ini] build_flags = -D PICO_USB_HOST ... load lib as host      
                print('  * TINYUSB      : HOST')
                env.BuildSources( OBJ_DIR, USB_DIR, src_filter = [ "+<*>", "-<device>", "+<class>" ] )
            else: 
                #[ini] build_flags = -D PICO_USB_DEVICE / PICO_STDIO_USB ... load lib as device      
                print('  * TINYUSB      : DEVICE')        
                env.BuildSources( OBJ_DIR, USB_DIR, src_filter = [ "+<*>", "-<host>", "+<class>" ] )            
            break


def add_sdk(env):
    add_ops(env)
    add_tinyusb(env)
    if 'ARDUINO' != env.get("PROGNAME"):
        new_delete = "+"
        pico_malloc = '+'
    else:
        new_delete = "-"
        pico_malloc = '-'
    filter = [ "+<*>",
        "-<lib>",
        "-<boot_stage2>",
        "-<pico/pico_cyw43_arch>",
        "-<pico/pico_lwip>",
        "-<pico/pico_bit_ops>",
        "-<pico/pico_divider>",
        "-<pico/pico_int64_ops>",
        "-<pico/pico_printf>",
        "-<pico/pico_float>",
        "-<pico/pico_double>",
        "-<pico/pico_stdio>",
        "-<pico/pico_stdio_usb>",
        "-<pico/pico_stdio_uart>",
        "-<pico/pico_stdio_semihosting>",
        "-<pico/pico_mem_ops>",
        "-<pico/pico_standard_link/crt0.S>",
        new_delete + "<pico/pico_standard_link/new_delete.cpp>",
        pico_malloc + "<pico/pico_malloc>"
    ]
    env.BuildSources( join("$BUILD_DIR", env.platform, env.sdk), join(env.framework_dir, env.sdk), src_filter = filter )
