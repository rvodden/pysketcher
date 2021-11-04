============
 PySketcher
============

.. image:: https://github.com/rvodden/pysketcher/workflows/Tests/badge.svg
    :target: https://github.com/rvodden/pysketcher/actions?query=workflow%3ATests+branch%3Amaster

.. image:: https://badgen.net/pypi/v/pysketcher?icon=pypi
       :target: https://pypi.org/project/pysketcher/

.. image:: https://api.codeclimate.com/v1/badges/eae2c2aa97080fbfed7e/maintainability
    :target: https://codeclimate.com/github/rvodden/pysketcher/maintainability

.. image:: https://codecov.io/gh/rvodden/pysketcher/branch/master/graph/badge.svg?token=AHCKOL75VY
    :target: https://codecov.io/gh/rvodden/pysketcher

.. image:: https://readthedocs.org/projects/pysketcher/badge/?version=latest&style=flat
    :target: https://pysketcher.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/hypothesis-tested-brightgreen.svg
    :target: https://hypothesis.readthedocs.io/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://badgen.net/github/dependabot/rvodden/pysketcher?icon=github
    :target: https://github.com/rvodden/pysketcher

----

Please note: **pysketcher is in alpha stage:** the interface is likely to change from release to release.

----

PySketcher makes creating precise, but simple **mechanics**, and **physics** diagrams
easy. It is published on pypi, and uses of the tools provided by the ``matplotlib`` library.
PySketcher is a modern Python library that makes creating precise, but simple **mechanics**, and **physics** diagrams
easy. It is published on pypi, and uses of the tools provided by the ``matplotlib`` library.

PySketcher is built upon the `legacy <https://github.com/hplgit/pysketcher>`_ of *Hans Petter Langtangen* who sadly passed away in 2016.
If you were familiar with his work, the current version includes the following changes:

#. The code is organised into multiple files.
#. The ``MatlibplotDraw`` object is decoupled from the ``Shape`` object, and no longer global.
#. ``Shape`` objects are immutable: a transformation returns a new ``Shape`` that is a transformed clone of the original.
#. Angles are expressed in radians.
#. The ``Composition`` object is used consistently to allow for assemblies of ``Shapes`` without code repetition.

`Please see the documentation for more information <https://pysketcher.readthedocs.io/en/latest/index.html>`_.
