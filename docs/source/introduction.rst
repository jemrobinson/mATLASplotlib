Introduction
============

This package is meant to be a simple wrapper around ``matplotlib`` for users who want to produce plots conforming to the style guide of the ATLAS experiment at the LHC.
Rather than interacting with ``matplotlib`` classes directly, these are managed through a :py:class:`canvas <.BaseCanvas>` class which has methods related to the plotting and styling of datasets and then writing the resulting output to graphical formats on disk.
