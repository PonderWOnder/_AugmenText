Installation
============

Installation is via ``pip``:

.. code-block:: bash

    pip install Augmentor

Required Packages
-----------------
To use Augmentext you need at least the following packages:

* numpy
* BeautifulSoup
* nltk

Building
--------

If you prefer to build the package from source, first clone the repository: 

.. code-block:: bash

    git clone https://github.com/mdbloice/Augmentext.git

Then enter the ``Augmentor`` directory and build the package:

.. code-block:: bash

    cd Augmentext
    python setup.py install

Alternatively you can first run ``python setup.py build`` followed by ``python setup.py install``. This can be useful for debugging.

.. attention::

    If you are compiling from source you may need to compile the dependencies also, including Pillow. On Linux this means having libpng (``libpng-dev``) and zlib (``zlib1g-dev``) installed.