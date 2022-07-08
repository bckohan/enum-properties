.. _Poetry: https://python-poetry.org/
.. _Pylint: https://www.pylint.org/
.. _isort: https://pycqa.github.io/isort/
.. _mypy: http://mypy-lang.org/
.. _django-pytest: https://pytest-django.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _readthedocs: https://readthedocs.org/
.. _me: https://github.com/bckohan
.. _npm: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

Contributing
############

Contributions are encouraged and welcome!! Please use the issue page to submit feature requests or
bug reports. Issues with attached PRs will be given priority and have a much higher likelihood of
acceptance. Please also open an issue and associate it with any submitted PRs.

We are actively seeking additional maintainers. If you're interested, please contact me_.


Installation
------------

`django-render-static` uses Poetry_ for environment, package and dependency management. Poetry_
greatly simplifies environment bootstrapping. Once it's installed.

.. code-block::

    poetry install -E all

External Dependencies
~~~~~~~~~~~~~~~~~~~~~

Some of the tests require npm_ to be installed.

Documentation
-------------

`django-render-static` documentation is generated using Sphinx_ with the readthedocs_ theme. Any
new feature PRs must provide updated documentation for the features added. To build the docs run:

.. code-block::

    cd ./doc
    poetry run make html


Static Analysis
---------------

`django-render-static` uses mypy_ for static type analysis, and Pylint_ for python linting.
Header imports are also standardized using isort_. Before any PR is accepted the following must be
run, and static analysis tools should not produce any errors or warnings. Disabling certain errors
or warnings where justified is acceptable:

.. code-block::

    poetry run isort render_static
    poetry run mypy render_static
    poetry run pylint render_static
    poetry run doc8 -q doc
    poetry check
    poetry run pip check
    poetry run safety check --full-report
    poetry run python -m readme_renderer ./README.rst


Running Tests
-------------

`django-render-static` is setup to use django-pytest_ to allow pytest_ to run Django unit tests.
All the tests are housed in render_static/tests/tests.py. Before a PR is accepted, all
tests must be passing and the code coverage must be at 100%.

To run the full suite:

.. code-block::

    poetry run pytest

To run a single test, or group of tests in a class:

.. code-block::

    poetry run pytest <path_to_tests_file>::ClassName::FunctionName

For instance to run all tests in DefinesToJavascriptTest, and then just the test_classes_to_js test
you would do:

.. code-block::

    poetry run pytest render_static/tests/tests.py::DefinesToJavascriptTest
    poetry run pytest render_static/tests/tests.py::DefinesToJavascriptTest::test_classes_to_js

