import platforminfo
import strings

import sys

VERSION = "1.0.0-beta5"
computer = platforminfo.Platform()


def picli():
    arg = sys.argv[1]

    if arg == "-help":
        print(strings.HelpPrint(VERSION))
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
