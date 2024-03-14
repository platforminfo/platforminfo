import platforminfo
import sys

VERSION = "1.0.0beta5.post2"
computer = platforminfo.Platform()


def picli():
    help_string = (f"""
PlatformInfo version {VERSION}
------------------------------------------------------------
Arguments:
------------------------------------------------------------
-cpuinfo             | Returns all CPU info
-logical_cores       | Returns number of logical cores
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
        return computer.ram({sys.argv[2]})
