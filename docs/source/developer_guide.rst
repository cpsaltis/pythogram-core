Developer guide
===============


Packaging
---------

Some word on relative paths in imports, taken from gram.py


Coding style
------------

Pythogram.core follows the PEP8 guidelines (http://www.python.org/dev/peps/pep-0008/). Compliance is checked with pep8 and pylint.

To install these tools in the virtualenv::

   ./bin/pip install pep8 pylint

To run pep8::

   ./bin/pep8 src/pythogram-core

To run pylint::

   ./bin/pylint src/pythogram-core


Functions in modules are ordered alphabetically. Todos are kept as inline comments e.g.::

	# TODO: thsis foo should be bar.

This way pylint can find them and report them.


Documentation
-------------

Pythogram-core uses sphinx (http://sphinx.pocoo.org/) for documentation. Mathematical formulas are rendered with Mathjax which is already included in the provided sphinx configuration file. 

To install sphinx in the virtualenv::

   ./bin/pip install sphinx

To build documentation in HTML::

   ./bin/sphinx-build src/pythogram-core/docs/source src/pythogram-core/docs/build


Testing
-------

Testing is vital to assure everything runs as expected. Pythogram-core uses nose for testing which provides a set of helpful tools.

To install nose in the virtualenv::

   ./bin/pip install nose coverage

To execute the tests::

   ./bin/nosetests src/pythogram-core

To check for coverage::

   ./bin/nosetests --with-coverage --cover-package=pythogram-core src/pythogram-core/
