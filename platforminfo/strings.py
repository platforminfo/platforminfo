def HelpPrint(version):
    return (f"""
PlatformInfo version {version}
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
