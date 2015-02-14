========
janome
========

.. note:: This is a skelton. NOT working.

Install
========

Strongly recommend install in a python virtual env.

.. code:: bash
		 
  (venv)$ python -V
  Python 3.4.2

  (venv) $ python setup.py install
  Finished processing dependencies for Janome==0.0.1

  (venv) $ pip freeze
  Janome==0.0.1

Run
====

.. code:: bash

  (venv) $ python
  >>> import janome
  >>> args = ['moco']
  >>> janome.main(args)
  Hello moco !
  Janome is a Japanese morphological analysis engine written by pure Python.

or

(venv) $ ./scripts/janome.sh 
Hello Anonymous !
Janome is a Japanese morphological analysis engine written by pure Python.

Test
======

.. code:: bash

  (venv) $ python tests/test_janome.py 
  .
  ----------------------------------------------------------------------
  Ran 1 test in 0.000s

  OK

Uninstall
===========

.. code:: bash

  (venv) $ pip uninstall janome
  Uninstalling Janome:
    /path/to/venv/lib/python3.4/site-packages/Janome-0.0.1-py3.4.egg
  Proceed (y/n)? y
    Successfully uninstalled Janome

