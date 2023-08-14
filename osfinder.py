# OSFinder v1.0.0
# Tejas Raman, 2023
# Licensed under MIT License

import sys
import os
import subprocess

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
    * macos_buildnumber (macOS only): Returns macOS build numbers (e.g `22A8380` for Ventura 13.0, 18F132 for 10.14.5)
    * kernelversion: returns kernel version (Windows vernel version and specific version number are the same)
    """
    def basePlatform():
        bases = {"win32": "windows", "darwin": "mac", "linux": "linux"}
        return bases[sys.platform]

    def baseKernel():
        kernels = {"linux": "linux", "darwin": "darwin", "windows": "nt"}
        return kernels[basePlatform()]

    def Parser(filename, to_be_cut, basestr):
        with open(filename) as file:
            x = dict()
            for line in file:
                x[line.split("=")[0]] = line.split(to_be_cut)[1]

            version = x[basestr].strip()
        return version

    # Main functions
    if args[0] == "basePlatform":
        return basePlatform()

    elif args[0] == "kernelversion":
        platform = basePlatform()
        if platform in ["mac", "linux"]:
            kernel = subprocess.Popen(['uname', '-r'], stdout=subprocess.PIPE)
            return kernel.stdout.read().strip().decode("utf-8")
        elif platform == "windows":
            pass

    elif args[0] == "arch":
        arch = subprocess.Popen(['uname', '-m'], stdout=subprocess.PIPE)
        return arch.stdout.read().strip().decode("utf-8")

    elif args[0] == "macos_buildnumber":
        platform = basePlatform()
        if platform != "mac":
            raise PlatformError(
                "macos_buildnumber function used on a non-Macintosh system")
        else:
            buildnum_sp = subprocess.Popen(
                ['sw_vers -buildVersion'], shell=True, stdout=subprocess.PIPE)
            # stdout adds newlines and is in binary format by default, string format needed
            buildnum = buildnum_sp.stdout.read().decode("utf-8").strip()
            return buildnum

    elif args[0] == "baseKernel":
        return baseKernel()

    elif args[0] == "osver":
        # Function to determine base OS version (see above)
        platform = basePlatform()

        if platform == "linux":

            ######################################################################
            # Linux platform version check. Checks os-release and/or LSB release #
            ######################################################################

            # Most OSes based on systemd have this file, plus some that are not systemd (e.g Devuan).
            # ID = distro name, VERSION_ID = version number

            if os.path.isfile("/etc/os-release"):
                return Parser('/etc/os-release', '=', 'VERSION_ID')

            elif os.path.isfile("/usr/lib/os-release"):
                return Parser('/usr/lib/os-release', '=', 'VERSION_ID')

            elif os.path.isfile("/etc/lsb-release"):
                return Parser('/etc/lsb-release', '=', 'DISTRIB_RELEASE')

            elif os.path.isfile("/usr/bin/lsb-release"):
                version_sp = subprocess.Popen(
                    ['/usr/bin/lsb_release -r'], shell=True, stdout=subprocess.PIPE)
                # splits output in colon, strips ot if spaces. stdout adds newlines and is in binary format by default, string format needed
                version = (version_sp.stdout.read().decode(
                    "utf-8").split(":"))[1].strip()

                return version

        elif platform == "mac":

            ###########################################################
            # macOS platform version check. Uses subprocess + sw_vers #
            ###########################################################

            version_sp = subprocess.Popen(
                ['sw_vers -productVersion'], shell=True, stdout=subprocess.PIPE)
            # stdout adds newlines and is in binary format by default, string format needed
            version = version_sp.stdout.read().decode("utf-8").strip()
            return version

        elif platform == "windows":
            # implement `wmic os get Caption,CSDVersion /value` for windows versions: buildver is still 10 on 11, writing a parser is too hard
            version_sp = subprocess.Popen(
                "wmic os get Name /VALUE", shell=True, stdout=subprocess.PIPE)
            version = (version_sp.stdout.read().decode(
                'utf-8').strip().split('|'))[0].split("=")[1]
            return version


print(rawOSInfo("osver"))
