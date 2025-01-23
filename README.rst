######################
Step size optimization
######################

This repository is focused on investigating numerical methods to determine optimal step sizes used for finite difference (FD) computations.
Example problems will be included to compare numerical methods against one another.

************
Installation
************

Cloning the repository
======================

.. code-block::
   
   $ git clone git@github.com:aaronriostx/step-size-optimization.git

Conda environment
=================

1. Create and activate the conda environment with the supplied ``environment.yml`` file:

.. code-block::
   
   $ conda create -f environment.yml
   $ conda activate step-size-opt-env

2. It is recommended to update the conda environment upon startup to ensure up-to-date dependencies:

..code-block::

   $ conda env update
