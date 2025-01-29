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

# Empty defaults list to avoid building all simulation targets by default
env.Default()

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

# Make the project package importable for: (1) SConscript files and (2) Python environments
sys.path.insert(0, str(project_dir))
env.PrependENVPath("PYTHONPATH", project_dir)

# Add WAVES builders
env.Append(
    BUILDERS={
        "CondaEnvironment": waves.scons_extensions.conda_environment(),
    }
)
env.Append(SCANNERS=waves.scons_extensions.sphinx_scanner())

# Dump the Conda environment as documentation of as-built target environment
environment_target = env.CondaEnvironment(
    target=[env["variant_dir_base"] / "environment.yaml"],
    source=[],
)
env.AlwaysBuild(environment_target)
env.Alias("environment", environment_target)

# Add documentation target(s)
# Project documentation
build_dir = env["variant_dir_base"] / documentation_source_dir
SConscript(
    documentation_source_dir / "SConscript",
    variant_dir=build_dir,
    exports={"env": env, "project_variables": project_variables},
)

# Add default target list to help message
# Add aliases to help message so users know what build target options are available
# This must come *after* all expected Alias definitions and SConscript files.
env.ProjectHelp()