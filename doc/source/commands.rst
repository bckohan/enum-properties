.. _ref-commands:

========
Commands
========

.. _renderstatic:

renderstatic
------------

.. automodule:: render_static.management.commands.renderstatic

Usage
~~~~~

.. argparse::
    :module: render_static.management.commands.renderstatic
    :func: get_parser
    :prog: manage.py

Example
~~~~~~~

To generate all templates configured in ``STATIC_TEMPLATES`` settings:

.. code::

    $ manage.py renderstatic

Alternatively individual templates can be generated, regardless of their presence
in ``STATIC_TEMPLATES``. They will be given the global context with any overriding context
parameters supplied on the command line:

.. code::

    $ manage.py renderstatic path/*.js -c ./js_context.yaml -d outputdir
