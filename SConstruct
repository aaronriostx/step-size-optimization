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

# Inherit user's full environment and set project options
env = waves.scons_extensions.WAVESEnvironment(
    ENV=os.environ.copy(),
    variant_dir_base=pathlib.Path(GetOption("variant_dir_base")),
    unconditional_build=GetOption("unconditional_build"),
    TARFLAGS="-c -j",
    TARSUFFIX=".tar.bz2",
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

# Set project configuration to dictionary
project_variables = {
    "project_configuration": project_configuration,
    "project_dir": project_dir,
    "project_name": project_name,
    "version": version,
    "author_list": author_list,
    "author_html": ", ".join(author for author in author_list),
    "author_latex": author_latex,
    "documentation_pdf": f"{latex_project_name}-{version}.pdf",
    "report_pdf": f"{latex_project_name}-{version}-report.pdf",
    "documentation_abspath": project_dir / documentation_source_dir,
}
for key, value in project_variables.items():
    env[key] = value