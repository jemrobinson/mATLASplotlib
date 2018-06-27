mATLASplotlib
=============
.. image:: https://travis-ci.org/jemrobinson/mATLASplotlib.svg?branch=master
   :target: https://travis-ci.org/jemrobinson/mATLASplotlib

.. image:: https://landscape.io/github/jemrobinson/mATLASplotlib/master/landscape.svg?style=flat
   :target: https://landscape.io/github/jemrobinson/mATLASplotlib/master
   :alt: Code Health

This package provides wrappers around matplotlib functionality produce plots compatible with the style guidelines for the ATLAS experiment at the LHC.
It is particularly aimed at users who are not familiar with matplotlib syntax.
Basic usage involves creating a canvas, plotting a dataset and saving the output to a file.
For example, something like

::

    from mATLASplotlib import canvases
    canvas = canvases.Simple(shape="rectangular")
    x, y = [0, 1, 2, 3], [0, 1, 4, 9]
    canvas.plot_dataset(x, y, style="scatter", label="Example points", colour="black")
    canvas.save_to_file("simple_example")

will produce a minimal scatter plot with automatically determined axis limits and save this to a PDF (if not otherwise specified).


Examples
========
Examples which reproduce the plots on this page (https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/PubComPlotStyle) are included in the `examples` folder.


Font setup
==========
To allow matplotlib to use Helvetica (required for ATLAS style) follow the guidelines from here http://blog.olgabotvinnik.com/blog/2012/11/15/2012-11-15-how-to-set-helvetica-as-the-default-sans-serif-font-in/ (reproduced below). For Linux users, adding the .ttf fonts to ~/.fonts and removing ~/.matplotlib/fontList.cache ~/.matplotlib/fontManager.cache ~/.matplotlib/ttffont.cache should be enough.

1. Download and install Fondu to convert Mac-Helvetica to ttf-Helvetica
`brew install fondu`

2. Find Helvetica on your system
Probably somewhere like: `/System/Library/Fonts/Helvetica.dfont`

3. Find where matplotlib stores its data

At python prompt run: `import matplotlib; matplotlib.matplotlib_fname()`
and get output like: `u'/usr/local/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc'`

We need to put the `.ttf` in this path in `fonts/ttf`

4. Create the `.ttf`
`sudo fondu -show /System/Library/Fonts/Helvetica.dfont`

5. Edit your `.matplotlibrc` file
Edit `~/.matplotlib/matplotlibrc`, find the line `font.sans-serif : Bitstream Vera Sans, ...` and put `Helvetica` at the beginning of this list

6. Force matplotlib to re-scan the font lists
Now we need to force matplotlib to re-create the font lists by removing the files.
`rm ~/.matplotlib/fontList.cache ~/.matplotlib/fontManager.cache ~/.matplotlib/ttffont.cache`

API
===

.. toctree::
    :maxdepth: 2

    source/canvases
    source/converters
    source/decorations
    source/plotters
    source/style
    source/matplotlib_wrapper


