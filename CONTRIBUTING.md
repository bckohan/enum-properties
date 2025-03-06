# Contributing

Contributions are encouraged! Please use the issue page to submit feature requests or bug reports. Issues with attached PRs will be given priority and have a much higher likelihood of acceptance. Please also open an issue and associate it with any submitted PRs. The aim is to keep this library as lightweight as possible. Only features with broad based use cases will be considered.

We are actively seeking additional maintainers. If you're interested, please contact [me](https://github.com/bckohan).


## Installation

### Install Just

We provide a platform independent justfile with recipes for all the development tasks. You should [install just](https://just.systems/man/en/installation.html) if it is not on your system already.

`enum-properties` uses [uv](https://docs.astral.sh/uv) for environment, package and dependency management:

```bash
    just install_uv
```

Next, initialize and install the development environment:

```bash
    just setup
    just install
```

## Documentation

`enum-properties` documentation is generated using [Sphinx](https://www.sphinx-doc.org). Any new feature PRs must provide updated documentation for the features added. To build the docs run:

```bash
    just install-docs
    just docs
```

Or to serve a live automatic rebuilding on localhost:

```bash
    just docs-live
```


## Static Analysis

`enum-properties` uses [ruff](https://docs.astral.sh/ruff) for python linting and formatting. [mypy](http://mypy-lang.org) and [pyright](https://github.com/microsoft/pyright) are used for static type checking. Before any PR is accepted the following must be run, and static analysis tools should not produce any errors or warnings. Disabling certain errors or warnings where justified is acceptable:

```bash
    just check
```

## Running Tests

`enum-properties` uses [pytest](https://docs.pytest.org/) to define and run tests. All the tests are housed under ``tests/``. Before a PR is accepted, all tests must be passing and the code coverage must be at 100%. A small number of exempted error handling branches are acceptable.

To run the full suite:

```bash
    just test
```

To run a single test, or group of tests in a class:

```bash
    just test <path_to_tests_file>::ClassName::FunctionName
```

For instance to run all tests in TestFlags, and then just the
test_int_flag example test you would do:

```bash
    just test tests/annotations/test_flags.py::TestFlags
    just test tests/annotations/test_flags.py::TestFlags::test_int_flag
```
