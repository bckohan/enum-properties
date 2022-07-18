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

Contributions are encouraged! Please use the issue page to submit feature
requests or bug reports. Issues with attached PRs will be given priority and
have a much higher likelihood of acceptance. Please also open an issue and
associate it with any submitted PRs. That said, the aim is to keep this library
as lightweight as possible. Only features with broad based use cases will be
considered.

We are actively seeking additional maintainers. If you're interested, please
contact me_.


Installation
------------

`enum-properties` uses Poetry_ for environment, package and dependency
management. Poetry_ greatly simplifies environment bootstrapping. Once it's
installed:

.. code-block::

    poetry install

Documentation
-------------

`enum-properties` documentation is generated using Sphinx_ with the
readthedocs_ theme. Any new feature PRs must provide updated documentation for
the features added. To build the docs run:

.. code-block::

    cd ./doc
    poetry run make html


Static Analysis
---------------

`enum-properties` uses Pylint_ for python linting. Header imports are also
standardized using isort_. Static type checking is not done because the code
simply relies too heavily on metaprogramming for it to be useful. Before any
PR is accepted the following must be run, and static analysis tools should not
produce any errors or warnings. Disabling certain errors or warnings where
justified is acceptable:

.. code-block::

    poetry run isort enum_properties
    poetry run pylint enum_properties
    poetry run doc8 -q doc
    poetry check
    poetry run pip check
    poetry run safety check --full-report
    poetry run python -m readme_renderer ./README.rst


Running Tests
-------------

`enum-properties` is setup to use pytest_ to run unit tests. All the tests are
housed in enum_properties/tests/tests.py. Before a PR is accepted, all tests
must be passing and the code coverage must be at 100%. A small number of
exempted error handling branches are acceptable.

To run the full suite:

.. code-block::

    poetry run pytest

To run a single test, or group of tests in a class:

.. code-block::

    poetry run pytest <path_to_tests_file>::ClassName::FunctionName

For instance to run all tests in TestEnums, and then just the
test_properties_and_symmetry test you would do:

.. code-block::

    poetry run pytest enum_properties/tests/tests.py::TestEnums
    poetry run pytest enum_properties/tests/tests.py::TestEnums::test_properties_and_symmetry

