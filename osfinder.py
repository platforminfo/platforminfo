# OSFinder v1.0.0
# Tejas Raman, 2023
# Licensed under MIT License

import sys
import os
import subprocess

def rawOSInfo(ptype):
    """ Base function for remaining functions inside of this. You can create an _OSObject_ which will have various methods"""
    if ptype == "basePlatform":
        def basePlatform():
            bases = {"windows": "windows", "darwin": "mac", "linux": "linux"}
            return bases(sys.platform)
    elif ptype == "baseKernel":
        def baseKernel():
            kernels = {"linux": "linux", "darwin": "darwin", "windows": "nt"}
            return kernels(basePlatform())
        return baseKernel()
    elif ptype == "osver":
        # Function to determine base OS version (see above)
        platform = basePlatform()

        if platform == "linux":

            ######################################################################
            # Linux platform version check. Checks os-release and/or LSB release #
            ######################################################################

            # Most OSes based on systemd have this file, plus some that are not systemd (e.g Devuan). 
            # ID = distro name, VERSION_ID = version number

            # FIXME: turn this repetitive code into a function to parse files; specify input as line to be found #

            if os.path.isfile("/etc/os-release"):
                # Parses common os-release file
                with open('/etc/os-release') as file:
                    x = dict()
                    for line in file:
                        x[line.split("=")[0]] = line.split("=")[1]
                    
                    version = x['VERSION_ID'].strip()
                return version
     
            elif os.path.isfile("/usr/lib/os-release"):
                 # Some OSes have os-release in /usr/lib (uncommon)
                 with open('/usr/lib/os-release') as file:
                    x = dict()
                    for line in file:
                        x[line.split("=")[0]] = line.split("=")[1]
                    
                    version = x['VERSION_ID'].strip()
                 return version

            elif os.path.isfile("/etc/lsb-release"):
                 # LSB is usually a compatibility measure, but lsb parser added in the event that a compliant os-release is not found
                 with open('/etc/lsb-release') as file:
                    x = dict()
                    for line in file:
                        x[line.split("=")[0]] = line.split("=")[1]
                    
                    version = x['VERSION_ID'].strip()
                 return version
            

            elif os.path.isfile("/usr/bin/lsb-release"):
                version_sp = subprocess.Popen(['/usr/bin/lsb_release -r'], shell=True stdout=subprocess.PIPE)
                version = (version_sp.stdout.read().decode("utf-8").split(":"))[1].strip() # splits output in colon, strips ot if spaces. stdout adds newlines and is in binary format by default, string format needed

                return version
                
        
        elif platform == "mac":

            ###########################################################
            # macOS platform version check. Uses subprocess + sw_vers #
            ###########################################################

            version_sp = subprocess.Popen(['sw_vers -productVersion'], shell=True, stdout=subprocess.PIPE)
            version = version_sp.stdout.read().decode("utf-8").strip() # stdout adds newlines and is in binary format by default, string format needed
            return version
        
        elif platform == "windows":
            # implement `wmic os get Caption,CSDVersion /value` for windows versions: buildver is still 10 on 11, writing a parser is too hard
            