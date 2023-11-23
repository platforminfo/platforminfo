#!/usr/bin/env bash

#####################################################################
# this script formats all python files in the directory using yapf.  #
#  if yapf is not present on your system, run `pip install yapf`.   #
#####################################################################

yapf --style pep8 -i -r .