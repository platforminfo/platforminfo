# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import subprocess
import sys

# winreg is only available in the win32 python stdlib, so import is restricted to win32 to mitigate errors
if sys.platform == "win32":
    import winreg


def subprocess_postproc(x):
    return x.stdout.read().strip().decode("utf-8")


class PlatformError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def parse_file(filename, to_be_cut, basestr):
    with open(filename) as file:
        x = dict()
        for line in file.readlines():
            line_lst = [x.strip() for x in line.split(to_be_cut)]
            x[line_lst[0]] = line_lst[1]
            if line_lst[0] == basestr:
                break
        return x[basestr]


class Platform:

    def __init__(self):
        bases = {
            "win32": "windows",
            "darwin": "mac",
            "linux": "linux",
            "bsd": "bsd"
        }

        # finding platform:
        self.platform = bases[
            sys.platform] if sys.platform in bases.keys() else sys.platform

    def base_platform(self):
        return self.platform

    def desktop_environment(self):
        if self.platform not in ["linux", "bsd"]:
            raise PlatformError(
                'Desktop environment property used on a non-Linux/BSD system')
        else:
            return os.environ['XDG_CURRENT_DESKTOP']

    def kernel_version(self):
        if self.platform in ["mac", "linux", "bsd"]:
            kernel = subprocess.Popen("uname -r",
                                      shell=True,
                                      stdout=subprocess.PIPE)
            return subprocess_postproc(kernel)

        elif self.platform == "windows":
            version = ".".join((subprocess_postproc(
                subprocess.Popen(
                    "wmic os get version /VALUE",
                    stdout=subprocess.PIPE,
                )).split("|"))[0].split("=")[1].split(".")[:2])
            return version

    def os_architecture(self):
        if self.platform == "windows":
            arch = (os.environ['PROCESSOR_ARCHITECTURE']).upper()
            arches = {'AMD64': 'x86_64', 'ARM64': 'aarch64'}
            retval = arches[arch] if arch in arches else arch
            return retval
        else:
            return subprocess_postproc(
                subprocess.Popen("uname -m",
                                 shell=True,
                                 stdout=subprocess.PIPE))

    def build_number(self):
        if self.platform == "mac":
            buildnum = subprocess_postproc(
                subprocess.Popen("sw_vers -buildVersion",
                                 shell=True,
                                 stdout=subprocess.PIPE))
            return buildnum

        elif self.platform == "windows":
            access_registry = winreg.ConnectRegistry(None,
                                                     winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(
                access_registry,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            value = winreg.QueryValueEx(key, "CurrentBuild")
            return value
        else:
            raise PlatformError(
                "PlatformInfo: buildnumber function is only compatible with Macintosh and Windows-based systems"
            )

    def os_version(self):
        # BSD support here is WIP
        if self.platform in ["linux", "bsd"]:
            if os.path.isfile("/etc/os-release"):
                return parse_file("/etc/os-release", "=", "VERSION_ID")

            elif os.path.isfile("/usr/lib/os-release"):
                return parse_file("/usr/lib/os-release", "=", "VERSION_ID")

            if self.platform != "bsd":
                if os.path.isfile("/etc/lsb-release"):
                    return parse_file("/etc/lsb-release", "=",
                                      "DISTRIB_RELEASE")

                elif os.path.isfile("/usr/bin/lsb-release"):
                    version_sp = subprocess.Popen("/usr/bin/lsb_release -r",
                                                  shell=True,
                                                  stdout=subprocess.PIPE)
                    version = (subprocess_postproc(version_sp).split(":"))[1]
                    return version

        elif self.platform == "mac":
            return subprocess_postproc(
                subprocess.Popen("sw_vers -productVersion",
                                 shell=True,
                                 stdout=subprocess.PIPE))

        elif self.platform == "windows":
            version = (subprocess_postproc(
                subprocess.Popen(
                    "wmic os get Name /VALUE",
                    shell=True,
                    stdout=subprocess.PIPE)).split("|"))[0].split("=")[1]
            return version

    def cpu_prettyname(self):
        if self.platform == "linux":
            return (parse_file("/proc/cpuinfo", ":", "model name"))

        elif self.platform == "bsd":
            cpu = (subprocess_postproc(
                subprocess.Popen(
                    "sysctl hw.model", shell=True,
                    stdout=subprocess.PIPE)).split(":"))[1].strip()
            return cpu

        elif self.platform == "windows":
            access_registry = winreg.ConnectRegistry(None,
                                                     winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(
                access_registry,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            value = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
            return value
        elif self.platform == "mac":
            cpu = subprocess_postproc(
                subprocess.Popen(
                    "sysctl machdep.cpu.brand_string  ",
                    shell=True,
                    stdout=subprocess.PIPE)).split(":")[1].strip()
            return cpu

    def cpu_cores(self, coreop="none"):
        if coreop == "none":
            print("""
            Please specify a core type.
                  
            Options are:
              physical
              logical

            Syntax: \x1B[3mplatforminfo_class\x1B[0m.cpu_cores(coretype)
            """)
        else:
            if self.platform == "linux":
                coretypes = {"physical": 'cpu cores', "logical": 'siblings'}
                return int(parse_file("/proc/cpuinfo", ":", coretypes[coreop]))

            elif self.platform == "windows":
                coretypes_win = {
                    "physical": "NumberOfCores",
                    "logical": "NumberOfLogicalProcessors"
                }
                cores = subprocess_postproc(
                    subprocess.Popen(
                        f"wmic cpu get {coretypes_win[coreop]} /VALUE",
                        stdout=subprocess.PIPE,
                    )).split("=")[1]
                return cores

            elif self.platform == 'bsd':
                cores = int(
                    (subprocess_postproc(
                        subprocess.Popen(
                            "sysctl hw.ncpu",
                            shell=True,
                            stdout=subprocess.PIPE)).split(":"))[1].strip())

                if coreop == "physical":
                    return str(cores)
                else:
                    threads = int((subprocess_postproc(
                        subprocess.Popen(
                            "sysctl kern.smp.threads_per_core",
                            shell=True,
                            stdout=subprocess.PIPE)).split(":"))[1].strip())
                    return str(cores * threads)
            elif self.platform == "mac":
                coretypes_mac = {
                    "physical": "core_count",
                    "logical": "thread_count"
                }
                cores = subprocess_postproc(
                    subprocess.Popen(
                        f"sysctl machdep.cpu.{coretypes_mac[coreop]}",
                        shell=True,
                        stdout=subprocess.PIPE)).split(":")[1].strip()
                return cores

    def gpu_prettyname(self):
        if self.platform == "windows":
            access_registry = winreg.ConnectRegistry(None,
                                                     winreg.HKEY_LOCAL_MACHINE)
            key = winreg.OpenKey(
                access_registry,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\WinSAT")
            value = winreg.QueryValueEx(key, "PrimaryAdapterString")[0].strip()
            return value

        elif self.platform == "mac":
            #################################################
            #           Warning, slow code ahead            #
            #  This needs to be fixed. Maybe you can FIXME?  #
            #################################################
            gpu = subprocess_postproc(
                subprocess.Popen(
                    'system_profiler SPDisplaysDataType | grep "Chipset Model"',
                    shell=True,
                    stdout=subprocess.PIPE)).split(":")[1].strip()
            return gpu

        elif self.platform == "linux":
            gpu = subprocess_postproc(
                subprocess.Popen('glxinfo | grep Device',
                                 shell=True,
                                 stdout=subprocess.PIPE)).split(":")[1].split(
                                     "(")[0].strip()
            return gpu

    def ram(self, dataunit="none"):
        # dataunit code consists of the unit and the power. PlatformInfo raises the number to the power when converted.
        dataunits = {
            "KiB": [1024, 1],
            "MiB": [1024, 2],
            "GiB": [1024, 3],
            "TiB": [1024, 4],
            "PIB": [1024, 5],
            "EiB": [1024, 6],
            "KB": [1000, 1],
            "kB": [1000, 1],
            "MB": [1000, 2],
            "GB": [1000, 3],
            "TB": [1000, 4],
            "PB": [1000, 5],
            "EB": [1000, 6],
            "B": [1, 1]
        }

        if dataunit not in dataunits.keys():
            raise PlatformError("Invalid RAM dataunit specified")

        if self.platform == "windows":
            ram = subprocess_postproc(
                subprocess.Popen(
                    f"wmic ComputerSystem get TotalPhysicalMemory /VALUE",
                    stdout=subprocess.PIPE,
                )).split("=")[1]
            if dataunit == "B":
                return int(ram)
            else:
                return int(
                    ram) / dataunits[dataunit][0]**dataunits[dataunit][1]
        elif self.platform == 'linux':
            ram = parse_file("/proc/meminfo", ":", "MemTotal")
            x = ram.split()
            return (int(x[0]) * dataunits[x[1]][0]**dataunits[x[1]][1]
                    ) / dataunits[dataunit][0]**dataunits[dataunit][1]

        elif self.platform == "mac":
            ram = subprocess_postproc(
                subprocess.Popen(
                    "sysctl hw.memsize", shell=True,
                    stdout=subprocess.PIPE)).split(":")[1].strip()
            return int(ram) / dataunits[dataunit][0]**dataunits[dataunit][1]

        elif self.platform == "bsd":
            ram = int(
                (subprocess_postproc(
                    subprocess.Popen(
                        "sysctl hw.realmem",
                        shell=True,
                        stdout=subprocess.PIPE)).split(":"))[1].strip())
            return int(ram) / dataunits[dataunit][0]**dataunits[dataunit][1]
