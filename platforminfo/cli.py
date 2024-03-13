import platforminfo
import sys


def picli():
    x = platforminfo.Platform()
    print(x.cpu_cores("logical"))
