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

# Project internal variables
project_configuration = pathlib.Path(inspect.getfile(lambda: None))
project_dir = project_configuration.parent
project_name = project_dir.name
version = "0.1.0"
author_list = [
    "G. Aaron Rios",
]
author_latex = r" \and ".join(author_list)
latex_project_name = project_name.replace("_", "-")

# Project source directories
documentation_source_dir = pathlib.Path("docs")