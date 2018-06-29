Installation
============

1. Requirements
---------------
- ``Python`` 2.7 (not yet tested with Python 3 but it should work)
- ``ROOT`` with ``PyROOT`` enabled
- ``matplotlib``
- ``numpy``
- ``scipy``

mATLASplotlib is developed and tested on Linux and Mac.

2. Automatic installation with pip
----------------------------------
To install a released version of mATLASplotlib use ``pip``.

To install in your home directory:

.. code:: bash

    pip install --user mATLASplotlib

To install system-wide (requires root privileges):

.. code:: bash

    sudo pip install mATLASplotlib


3. Upgrading with pip
---------------------
To upgrade with ``pip`` simply do

.. code:: bash

    pip install -U mATLASplotlib

running with sudo as before if this is a system-wide installation


4. Installing from source
-------------------------
Clone the repository with ``git``:

.. code:: bash

    git clone https://github.com/jemrobinson/mATLASplotlib.git

After doing this, you should use the ``setup.py`` script to install.

To install in your home directory:

.. code:: bash

    python setup.py install --user

To install system-wide (requires root privileges):

.. code:: bash

    sudo python setup.py install