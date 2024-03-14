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
        print(help_string)
    elif arg == "-logical-cores":
        print(computer.cpu_cores("logical"))
    elif arg == "-physical-cores":
        print(computer.cpu_cores("physical"))
    elif arg == "-cpuname":
        print(computer.cpu_prettyname())
    elif arg == "-desktop-environment":
        print(computer.desktop_environment())
    elif arg == "-os-arch":
        print(computer.os_architecture())
    elif arg == "-kernel-version":
        print(computer.kernel_version())
    elif arg == "-os-version":
        print(computer.os_version())
    elif arg == "-buildnumber":
        print(computer.build_number())
    elif arg == "-gpuname":
        print(computer.gpu_prettyname())
    elif arg == "-ram":
        print(computer.ram({sys.argv[2]}))


picli()
