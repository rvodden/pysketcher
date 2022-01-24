##########################
Contributing to PySketcher
##########################

Code of Conduct
###############

This project and everyone participating in it is governed by the `PySketcher Code of Conduct <https://github.com/rvodden/pysketcher/blob/master/CODE_OF_CONDUCT.md>`_.

What should I know before I contribute?
#######################################

Coding Style
============

PySketcher is very opinionated about coding style. Our coding style is enforced in CI and can also be run locally
( see the build section below ). In addition, we use git pre-commit hooks to do rudimentary checks of style. These
can be configured in your local clone by running ``pre-commit install`` after you've installed the development
dependencies. This will prevent you from committing until you've complied with the requisite conventions. We largely
follow the ``Black`` coding style and as such many issues can be automatically resolved by running ``nox -s black``.

Documentation
=============

PySketcher is a library, as such our usability is largely down to the quality of our documentation. There are three
types of documentation within this project:

* DocStrings
* Examples
* The Tutorial (work in progress)

DocStrings
----------

Every public class and every public method of every public class must be documented in its DocString. Because there is nothing worse
than discovering documentation which doesn't work, PySketcher uses the ``pytest-doctest`` plugin to ensure that all
docstrings execute, and a few conventions to include the generated image (where appropriate) in the generated documentation.

The docstring environment will already have ``numpy``, ``matplotlib`` and ``pysketcher`` imported, to avoid unnecessary repetition.

Take, for example, the docstring from the ``Line`` class:

.. code-block:: python

    class Line(Curve):
        """A representation of a line primitive.
        Args:
            start: The starting point of the line.
            end: The end point of the line.
        Example:
            >>> a = ps.Line(ps.Point(1.0, 2.0), ps.Point(4.0, 3.0))
            >>> b = a.rotate(np.pi / 2, ps.Point(1.0, 2.0))
            >>> fig = ps.Figure(0, 5, 0, 5, backend=MatplotlibBackend)
            >>> fig.add(a)
            >>> fig.add(b)
            >>> fig.save("pysketcher/images/line.png")
        .. figure:: images/line.png
            :alt: An example of Line.
            :figclass: align-center
            An example of ``Line``.
        """

        ...

In general the docstring follows the
`Google Style for docstrings <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_
but with an explicit ``Example`` section which should have an interactive mode example of how to use the class. During
documentation generation, all images which are placed in ``pysketcher/images`` are copied to an ``images`` directory
within the documentation section. This means that, as shown in lines 13-15 above, any images which are saved in the
the docstring can, and indeed should, be included in the rendered documentation. `The rendered documentation for this
example can be viewed here <https://pysketcher.readthedocs.io/en/latest/modules.html#pysketcher.Line>`_.

Examples
--------

Examples should be informative demonstrations of how multiple parts of PySketcher can be used together. If one
considers docstrings to be analogous to unit tests, then examples could be considered analogous to integration tests.
The current set of examples are largely drawn from the set provided by the original author. The current maintainers
would love to find a way for each example to form a stand alone tutorial and form part of the rendered documentation.
This pipe dream is being tracked as `issue 384 <https://github.com/rvodden/pysketcher/issues/384>`_.

The Tutorial
------------

The tutorial is the last remaining big piece of work to complete before PySketcher can be considered feature complete
as compared to before the refactor. The effort to this end is being tracked as
`issue #2 <https://github.com/rvodden/pysketcher/issues/2>`_.

Build
=====

As mentioned before, PySketcher is a library and as such is must be built, packaged, and tested as one. This means that
its not good enough to just test that code works, but we must test that it works from a fresh install. This can be
slow though, so we've developed a workflow which we think is the right balance between comprehensive testing and
pace of development. The setup is based on Claudio Jolowicz's amazing 2000 article
`Hypermodern Python <https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769>`_

Local Build
-----------

The quickest way to test, and therefore the recommended method whilst a feature is actively being developed, is to set up
a virtual environment, install the dependencies into it, and run the tests from there. We'll illustrate this with
``virtualenv`` however any virtual environment manager should work.

.. code-block:: sh

    > python -m virtualenv .venv
    > . .venv/bin/activate
    > pip install poetry
    > poetry install
    > pytest

This will run the unit and docstring tests. Note that in PySketcher we consider the docstring tests to be unit
tests and they contribute to unit test coverage, so there is no need to duplicate if the code is genuinely the
same. It is, in general, unlikely that docstring tests do appropriate boundary checking, however.

Linting and style checks can be run by executing ``flake8`` followed by the target location:

.. code-block:: sh

    > flake8 pysketcher

If an error appears saying ``black would make changes`` then its likely that these can be automatically resolved:

.. code-block:: sh

    > black

Wheel Build
-----------

When ``pip`` or another package manager installs a python library, it downloads a "wheel" file, and installs the library
from that. As such is very important that we check that PySketcher works correctly when its installed from a wheel.
To do this we use ``nox``:

.. code-block:: sh

    > nox -s tests-3.9

This will build a wheel from the code on the current branch, create a fresh venv, install the wheel into it, and then
run the test suite. The ``3.9`` in this command specifies the python version. At any one time PySketcher supports 3
versions of Python - the latest, and the two prior to that. The next section describes how to test against all supported
versions.

Full Matrix Build
-----------------

As mentioned in the previous section, at any one time, PySketcher supports 3 versions of Python. The latest version
(3.10 at the time of writing) and the two previous versions (3.8 and 3.8). As such we must test against all versions
and nox will do this for us. This takes a reasonable amount of time (about 6 minutes at the time of writing) so its
probably worth leaving until you believe that your PR is ready for submission. It will also be run by the CI/CD process
which will also execute on Windows and Linux:

.. code-block:: sh

    > nox

Testing
=======

There is a large overlap between testing and the build and documentation sections above, so this section will
only speak to those topics which have not already been covered.

Bounds
------

Floating point math can be tricky, and a lot of coding effort can go into dealing with the extremes. As PySketcher
is primarily aimed to be a diagramming tool, with those diagrams intended for human consumption, it is unlikely
that extremes will come up in genuine use cases. As such, testing is restricted to angles with a magnitude which
exceeds $1 * 10 ^ {-30}$ and distances are kept below $1 * 10^30$. Similarly any values which are within $1 * 10 ^ {-4}$
are considered equal. These are entirely arbitrary values and use cases which require more precision will be welcomed -
please raise an issue with details so that they can be discussed.

Hypotheses
----------

Our tests all run using `Hypothesis <https://hypothesis.readthedocs.io/en/latest/manifesto.html>`_ This takes a bit of
getting used to, but it does end up with more reliable software. Every time we have thought we've found an issue
with Hypothesis it has ended up being a problem with our code which likely would never have been found otherwise. As you
contribute please look at the other tests for examples of how to use Hypothesis and ask for help through your issue.
In the ``tests.strategies`` package you will find strategies which obey the bounds outlined in the previous section.

How to contribute?
##################

Raising an issue
================

Contributions can take many forms. They can be as simple as a well written bug report, or as much as a complete refactor
of part of the code. They all start in the same way, however, with an issue. Issue is an unfortunate name, as it might
be that you have a suggestion, or that you have a use case which you don't think the authorship have considered.

Choosing an issue
=================

If you'd like to contribute some code then first of all THANK YOU! Secondly, please make it clear on the issue which
you've chosen that you'd like to work on it, and outline briefly the approach you intend to take. This will avoid
more than one person working on the same issue, which can be very frustrating on highly distributed projects.

Asking for help
===============

It might be that you get some way through working on your issue and you get stuck. If you'd like to ask us for help
then please feel free and do so by raising a PR and marking it as draft. This will mean that we know its not ready for
final review. Ask you question in a comment on the PR and we will do our best to help you out.

Submitting a PR
===============

We have quite a rigorous CI process which will automatically check your PR for you. We will not merge a PR until the CI
tests have passed. If you are having trouble getting a PR to pass its tests, then please feel free to mark the PR as
draft and ask us for help.
