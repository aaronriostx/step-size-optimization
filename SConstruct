#! /usr/bin/env python

import os
import sys
import pathlib
import inspect

import waves

# Accept command line options with fall back default values
AddOption(
    "--build-dir",
    dest="variant_dir_base",
    default="build",
    nargs=1,
    type="string",
    action="store",
    metavar="DIR",
    help="SCons build (variant) root directory. Relative or absolute path. (default: '%default')",
)
AddOption(
    "--unconditional-build",
    dest="unconditional_build",
    default=False,
    action="store_true",
    help="Boolean to force building of conditionally ignored targets. (default: '%default')",
)