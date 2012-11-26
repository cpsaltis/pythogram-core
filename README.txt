pythogram-core
==============

:Version: 0.0
:Author: Christodoulos Psaltis (cpsaltis)
:Source: https://github.com/photogrammetry/pythogram-core
:License: MIT
:Keywords: python, photogrammetry, artificial data, feature extraction, machine learning, classification

Pythogram-core is a wrapper of several popular image processing and machine learning libraries. It provides a helpful command line tool to run complex workflows. It makes easy to integrate with other systems since it can communicate and execute tasks from JSON task files. 

Before installing
-----------------
Pythogram-core requires python version > 2.6 and < 3.0. You'll need some basic libraries and tools depending on your OS.

In a Debian based distro you'll need to::

    sudo aptitude install build-essential python-dev gfortran libatlas-base-dev python-virtualenv python-pip git

In MacOSX you'll need to install:

* XCode and its command line tools,
* git
* pip and virtualenv
* a packaging manager like Homebrew or MacPorts

Pip and virtualenv can be easily installed from the command line with::

    sudo easy_install pip
    sudo pip install virtualenv

Assuming you're using Homebrew you'll need to::

    brew install jpeg libtiff gfortran

Installation
------------
Pythogram-core depends on:

* numpy and scipy for basic computations,
* pillow/PIL for image IO,
* scikit-image for feature extraction,
* and scikit-learn for machine learning 

To setup all of the above in a virtualenv::

    virtualenv pythogram-core
    cd pythogram-core
    ./bin/pip install numpy
    ./bin/pip install scipy
    ./bin/pip install cython
    ./bin/pip install pillow scikit-image scikit-learn
    ./bin/pip install -e git+https://cpsaltis@github.com/photogrammetry/pythogram-core.git#egg=pythogram-core

Note that the order of installation steps is important. Scipy 0.10.1 doesn't work with numpy 1.6.2, but 0.10.0 does. In scipy 0.11.0 this issue has been resolved.

Optionally iPython can be very helpful in prototyping::

    ./bin/pip install ipython

If you plan to contribute to Pythogram you'll also need::

    ./bin/pip install pep8 sphinx pylint nose