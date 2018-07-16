mATLASplotlib
=============
.. image:: https://travis-ci.org/jemrobinson/mATLASplotlib.svg?branch=master
   :target: https://travis-ci.org/jemrobinson/mATLASplotlib
   :alt: Travis Build

.. image:: https://landscape.io/github/jemrobinson/mATLASplotlib/master/landscape.svg?style=flat
   :target: https://landscape.io/github/jemrobinson/mATLASplotlib/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/github/jemrobinson/mATLASplotlib/badge.svg?branch=master
   :target: https://coveralls.io/github/jemrobinson/mATLASplotlib?branch=master
   :alt: Coverage

.. image:: https://badge.fury.io/py/mATLASplotlib.svg
   :target: https://badge.fury.io/py/mATLASplotlib
   :alt: pypi

This package provides wrappers around matplotlib functionality produce plots compatible with the style guidelines for the ATLAS experiment at the LHC.
It is particularly aimed at users who are not familiar with matplotlib syntax.
Basic usage involves creating a canvas, plotting a dataset and saving the output to a file.
For example, something like

::

    import mATLASplotlib
    with mATLASplotlib.canvases.Simple(shape="landscape") as canvas:
        x, y = [0, 1, 2, 3], [0, 1, 4, 9]
        canvas.plot_dataset(x, y, style="scatter", label="Example points", colour="black")
        canvas.save("simple_example")

will produce a minimal scatter plot with automatically determined axis limits and save this to a PDF (if not otherwise specified).


.. toctree::
    :maxdepth: 2

    source/introduction
    source/installation
    source/font_setup
    source/getting_started
    source/examples
    source/api
