# OSFinder v1.0.0
# Tejas Raman, 2023
# Licensed under MIT License

import sys
import os
import subprocess
import winreg

##########
# Fixes: #
##########

# FIXME: class object that does not require a platform check every time command is run


class PlatformError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def rawOSInfo(*args):
    """
    # OSFinder `rawOSinfo()` function
    Base function for remaining functions inside of this. You can create an _OSObject_ which will have various methods.
    ### Inputs:
    args[ptype. args] (args are optional unless specific output is needed (e.g general vs specific OS versions))
    ### Process Types
    * basePlatform: returns either `windows`, `mac`, or `linux` based on the system it is being run on. No arguments
    * baseKernel: returns `nt`, `darwin`, `linux` (REDUNDANT).
    * arch: returns processor architecture. Only supports linux or macOS for now
    * osver: returns os version string (takes arguments for whether you want specific version (e.g `12.6` or `10.0.22621.025`) or general version (e.g `12`(macOS 12), `11` (Windows 11)).
    If the OS does not have a  specific version (e.g Fedora), version is returned same as general version
    * servicepack (Windows only): returns Windows service pack and OS Version (e.g [`"7", "SP1"]` or `["11", "22H2]` for Windows 11 22h2)
    * buildnumber (macOS/Windows): Returns macOS build numbers (e.g `22A8380` for Ventura 13.0, 18F132 for 10.14.5) or Windows build numbers (e.g 22621 (11 22h2), 7602 (Winows 7 SP1), 17763 (Windows 10))
    * kernelversion: returns kernel version
    """

    def basePlatform():
        bases = {"win32": "windows", "darwin": "mac", "linux": "linux"}
        return bases[sys.platform]

    # Largely redundant; will be removved in the future
    # def baseKernel():
    #     kernels = {"linux": "linux", "darwin": "darwin", "windows": "nt"}
    #     return kernels[basePlatform()]

    def Parser(filename, to_be_cut, basestr):
        with open(filename) as file:
            x = dict()
            for line in file:
                x[line.split("=")[0]] = line.split(to_be_cut)[1]

            version = x[basestr].strip()
        return version

    def subprocess_postproc(x):
        return x.stdout.read().strip().decode("utf-8")

    # Main functions
    if args[0] == "basePlatform":
        return basePlatform()

    elif args[0] == "kernelversion":
        platform = basePlatform()

        if platform in ["mac", "linux"]:
            kernel = subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE)
            return subprocess_postproc(kernel)

        elif platform == "windows":
            version = ".".join((subprocess_postproc(
                subprocess.Popen(
                    "wmic os get version /VALUE",
                    shell=True,
                    stdout=subprocess.PIPE,
                )).split("|"))[0].split("=")[1].split(".")[:2])
            return version

    elif args[0] == "arch":
        if platform in ["mac", "linux"]:
            return subprocess_postproc(
                subprocess.Popen(["uname", "-m"], stdout=subprocess.PIPE))

    elif args[0] == "buildnumber":
        platform = basePlatform()
        if platform not in ["mac", "windows"]:
            raise PlatformError("PlatformInfo: buildnumber function used on a non-Macintosh/Windows system")
        else:
            if platform == "mac":
                buildnum = subprocess_postproc(
                    subprocess.Popen("sw_vers -buildVersion",shell=True,stdout=subprocess.PIPE))
                return buildnum

            elif platform == "windows":
                access_registry = winreg.ConnectRegistry(
                    None, winreg.HKEY_LOCAL_MACHINE)
                key = winreg.OpenKey(
                    access_registry,
                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                value, type = winreg.QueryValueEx(key, "CurrentBuild")
                return value

    # elif args[0] == "baseKernel":
    #     return baseKernel()

    # Largely redundant functionality

    elif args[0] == "osver":
        platform = basePlatform()

        if platform == "linux":
            if os.path.isfile("/etc/os-release"):
                return Parser("/etc/os-release", "=", "VERSION_ID")

            elif os.path.isfile("/usr/lib/os-release"):
                return Parser("/usr/lib/os-release", "=", "VERSION_ID")

            elif os.path.isfile("/etc/lsb-release"):
                return Parser("/etc/lsb-release", "=", "DISTRIB_RELEASE")

            elif os.path.isfile("/usr/bin/lsb-release"):
                version_sp = subprocess.Popen("/usr/bin/lsb_release -r",
                                              shell=True,
                                              stdout=subprocess.PIPE)
                version = (subprocess_postproc(version_sp).split(":"))[1]
                return version

        elif platform == "mac":
            return subprocess_postproc(
                subprocess.Popen(["sw_vers -productVersion"],
                                 shell=True,
                                 stdout=subprocess.PIPE))

        elif platform == "windows":
            version = (subprocess_postproc(
                subprocess.Popen(
                    "wmic os get Name /VALUE",
                    shell=True,
                    stdout=subprocess.PIPE)).split("|"))[0].split("=")[1]
            return version
