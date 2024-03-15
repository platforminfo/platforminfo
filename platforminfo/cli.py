import platforminfo
import sys
from importlib.metadata import version


VERSION = version("plarforminfo")
computer = platforminfo.Platform()

RAMUNITS = {'KiB', 'MiB', 'GiB', 'TiB', 'PIB', 'EiB',
            'KB', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'B'}

ARGS_ALLOWED = {"-cpuinfo", "-logical-cores", "-physical-cores", "-cpuname",
                "-desktop-environment", "-os-arch", "-build-number", "-gpuname", "-ram", "-version"}


def picli():

    if len(sys.argv) < 2 or sys.argv[1] not in ARGS_ALLOWED:
        print("""
Usage: platform [arguments] [parameters]
To view all arguments, use\x1B[3m platforminfo -help\x1B[0m
""")
        sys.exit()

    help_string = (f"""
PlatformInfo version {VERSION}
------------------------------------------------------------
Arguments:
------------------------------------------------------------
-cpuinfo             | Returns all CPU info
-logical-cores       | Returns number of logical cores
-physical-cores      | Returns number of physical cores
-cpuname             | Returns CPU vendoe string (name)
-desktop-environment | Returns desktop environment (Linux/BSD)
-os-arch             | Returns OS architecture
-kernel-version      | Returns kernel version string
-os-version          | Returns OS version
-build-number        | Returns OS build number (Windows/macOS)
-gpuname             | Returns GPU vendor string (name)
-ram \x1B[3m dataunit \x1B[0m      | Returns ram in specified unit
    """)

    arg = sys.argv[1]

    if arg == "-help":
        return help_string
    elif arg == "-version":
        return VERSION
    elif arg == "-logical-cores":
        return computer.cpu_cores("logical")
    elif arg == "-physical-cores":
        return computer.cpu_cores("physical")
    elif arg == "-cpuname":
        return computer.cpu_prettyname()
    elif arg == "-desktop-environment":
        return computer.desktop_environment()
    elif arg == "-os-arch":
        return computer.os_architecture()
    elif arg == "-kernel-version":
        return computer.kernel_version()
    elif arg == "-os-version":
        return computer.os_version()
    elif arg == "-buildnumber":
        return computer.build_number()
    elif arg == "-gpuname":
        return computer.gpu_prettyname()
    elif arg == "-ram":
        if sys.argv[2].strip() not in RAMUNITS:
            print("""
Invalid RAM units or no unit provided.
To view syntax for this command, use\x1B[3m platforminfo -help\x1B[0m
""")
            sys.exit()
        else:
            return computer.ram({sys.argv[2]})
