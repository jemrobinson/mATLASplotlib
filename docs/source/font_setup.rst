Font setup
==========
To allow ``matplotlib`` to use Helvetica (required for ATLAS style) follow the guidelines from here http://blog.olgabotvinnik.com/blog/2012/11/15/2012-11-15-how-to-set-helvetica-as-the-default-sans-serif-font-in/ (reproduced below).

1. Linux users
--------------
For Linux users, adding the ``.ttf`` fonts to ``~/.fonts`` and removing ``~/.matplotlib/fontList.cache`` ``~/.matplotlib/fontManager.cache`` ``~/.matplotlib/ttffont.cache`` should be enough.


2. OSX users
------------
- Download and install ``fondu`` to convert Mac-Helvetica to ttf-Helvetica

.. code:: bash

    brew install fondu

- Find Helvetica on your system

Probably somewhere like: ``/System/Library/Fonts/Helvetica.dfont``

- Find where ``matplotlib`` stores its data

- Start a ``python`` prompt and run:

.. code:: python

    import matplotlib; matplotlib.matplotlib_fname()

and get output like:

.. code:: python

    u'/usr/local/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc'

we need to put the ``.ttf`` from this path in ``fonts/ttf``

- Create the ``.ttf``

.. code:: bash

    sudo fondu -show /System/Library/Fonts/Helvetica.dfont

- Edit your ``.matplotlibrc`` file

Edit ``~/.matplotlib/matplotlibrc``, find the line ``font.sans-serif : Bitstream Vera Sans, ...`` and put ``Helvetica`` at the beginning of this list

- Force matplotlib to re-scan the font lists

Now we need to force matplotlib to re-create the font lists by removing the files.

.. code:: bash

    rm ~/.matplotlib/fontList.cache ~/.matplotlib/fontManager.cache ~/.matplotlib/ttffont.cache