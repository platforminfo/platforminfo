<span> <p align="center"> <img src="https://platforminfo.github.io/img/docusaurus.png"><h1>PlatformInfo <i>beta</i></h1></span>
<span>![CircleCI](https://img.shields.io/circleci/build/github/platforminfo/platforminfo/development?style=for-the-badge&label=DEVELOPMENT%20BUILD&labelColor=6f6f6f)
![CircleCI](https://img.shields.io/circleci/build/github/platforminfo/platforminfo/main?style=for-the-badge&label=STABLE%20BUILD&labelColor=%236f6f6f)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/platforminfo?style=for-the-badge&labelColor=ad9b00)
![PyPI - Version](https://img.shields.io/pypi/v/platforminfo?style=for-the-badge&label=PyPi%20version&labelColor=%23ad9b00)
![GitHub](https://img.shields.io/github/license/platforminfo/platforminfo?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/platforminfo?style=for-the-badge&label=Downloads%20(past%20month%2C%20excl.%20mirrorbots)&labelColor=%23ad9b00)

</span>

[![asciicast](https://asciinema.org/a/606618.svg)](https://asciinema.org/a/606618)

System info for Python made simple.
PlatformInfo is designed to provide a simple, yet granular interface to find system information on all major operating systems within Python.

## Features:

*  Return kernel AND kernel version for Mac, Windows, Linux
*  Return OS versions for Windows, Mac, Linux
*  Return OS build numbers for Windows, Mac
*  Return desktop environments
*  Return architecture (Linux/Mac only, Windows planned)

## Prerequisites
*  Python 3 or up

## Installation:
To install PlatformInfo, you can download install it with pip (recommended) or install it from the development wheel.

**PyPi install (recommended):**
`pip install platforminfo`

**Manual install**
Download it from our [Development CI](https://app.circleci.com/pipelines/github/platforminfo/platforminfo?branch=development) and run `pip install /path/to/platforminfo-nightly.whl'

## Quick Start Guide:
TO start, import platforminfo and create a `Platform` object

```python
import platforminfo
computer = platforminfo.Platform()
```

To access information, find the name of the information you want (in this example I want `osVersion`).

```python
import platforminfo
computer = platforminfo.Platform()

value = computer.osVersion()
```

## Feature Requests
If you have a suggestion, [feel free to submit a feature request](https://github.com/platforminfo/platforminfo/issues).
You can grab the nightly builds on our [Development CI](https://app.circleci.com/pipelines/github/platforminfo/platforminfo?branch=development)
