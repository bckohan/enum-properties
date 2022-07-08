.. _ref-configuration:

=============
Configuration
=============

`django-render-static` settings are set in the ``STATIC_TEMPLATES`` dictionary in your site
settings:

.. code-block:: python

      STATIC_TEMPLATES = {
        'ENGINES': [
            'BACKEND': 'render_static.backends.StaticDjangoTemplates',
            'DIRS': [BASE_DIR / 'tmpls' ], # look here for templates
            'OPTIONS': {
                'app_dir': 'static_templates',  # search this directory in apps for templates
                'loaders': [
                    # search apps for templates
                    'render_static.loaders.StaticAppDirectoriesBatchLoader',
                    # search DIRS for templates
                    'render_static.loaders.StaticFilesystemBatchLoader'
                 ],
                'builtins': ['render_static.templatetags.render_static']
            },
        ],
        'context': {
            # define a global context dictionary that will be used to render all templates
        },
        'templates' {
            'app/js/defines.js': {
                'context': {
                    'defines': 'app.defines.DefinesClass'
                }
            },
            'urls.js': {}
        }
      }

The ``STATIC_TEMPLATES`` setting closely mirrors the ``TEMPLATES`` setting by defining which
template backends should be used. It extends the standard setting with a few options needed by the
static engine including a global context available to all static templates and a set of template
specific configuration parameters. It's advisable to first read about Django's ``TEMPLATES``
setting. The main difference with ``STATIC_TEMPLATES`` is that it supports batch rendering.
Glob-like patterns can be used to select multiple templates for rendering. See :ref:`loaders` for
more details.

Minimal Configuration
---------------------

To run `renderstatic`, ``STATIC_TEMPLATES`` must be defined in settings. If it's an empty
dictionary (or None):

.. code-block:: python

    STATIC_TEMPALTES = {}


then the default engine and loaders will be used which is equivalent to:

.. code-block:: python

    STATIC_TEMPALTES = {
        'ENGINES': [{
            'BACKEND': 'render_static.backends.StaticDjangoTemplates',
            'OPTIONS': {
                'loaders': ['render_static.loaders.StaticAppDirectoriesBatchLoader'],
                'builtins': ['render_static.templatetags.render_static']
            },
        }]
    }



``ENGINES``
-----------

A prioritized list of backend template engines and their parameters. The engines at the front of the
list have precedence over engines further down the list. The ``ENGINES`` parameters are
inherited from the standard Django ``TEMPLATES`` configuration.

``BACKEND``
~~~~~~~~~~~
The backend classes that render templates. The standard ``TEMPLATES`` engines should not be used
here, instead use the two engines provided by `django-render-static`:

- ``render_static.backends.StaticDjangoTemplates``
    - default app directory: ``static_templates``
- ``render_static.backends.StaticJinja2Templates``
    - default app directory: ``static_jinja2``

If ``APP_DIRS`` is true, or if an app directories loader is used such that templates are searched
for in apps then the default app directories listed above are where templates should reside. Unlike
the standard Django backends, the app directory location can be changed by passing the ``app_dir``
parameter into ``OPTIONS``.

``OPTIONS``
~~~~~~~~~~~

A list of configuration parameters to pass to the backend during initialization. Most of these
parameters are inherited from the standard Django template backends. One additional parameter
``app_dir`` can be used to change the default search path for static templates within apps.

.. _loaders:

``loaders``
***********

Works the same way as the ``loaders`` parameter on ``TEMPLATES``. Except when using the standard
template backend the loaders have been extended and static specific loaders should be used instead:

- ``render_static.backends.StaticDjangoTemplates``
    - ``render_static.loaders.django.StaticAppDirectoriesBatchLoader`` **default**
    - ``render_static.loaders.django.StaticFilesystemBatchLoader``
    - ``render_static.loaders.django.StaticAppDirectoriesLoader``
    - ``render_static.loaders.django.StaticFilesystemLoader``
    - ``render_static.loaders.django.StaticLocMemLoader``

- ``render_static.backends.StaticJinja2Templates``
    - ``render_static.loaders.jinja2.StaticFileSystemBatchLoader`` **default**
    - ``render_static.loaders.jinja2.StaticFileSystemLoader``
    - ``render_static.loaders.jinja2.StaticPackageLoader``
    - ``render_static.loaders.jinja2.StaticPrefixLoader``
    - ``render_static.loaders.jinja2.StaticFunctionLoader``
    - ``render_static.loaders.jinja2.StaticDictLoader``
    - ``render_static.loaders.jinja2.StaticChoiceLoader``
    - ``render_static.loaders.jinja2.StaticModuleLoader``

.. note::
    The static template engine supports batch rendering. All loaders that have ``Batch`` in the name
    support wild cards and glob-like patterns when loading templates. By default, if no loaders are
    specified these loaders are used. For instance, if I wanted to render every .js file in a
    directory called static_templates/js I could configure templates like so:

.. code-block:: python

    'templates': {
        'js/*.js': {}
    }

``context``
-----------
Specify a dictionary containing the context to pass to any static templates as they render. This
is the global context that will be applied to all templates. Specific templates can override
individual context parameters, but not the whole dictionary. By default all contexts will have the
Django settings in them, keyed by ``settings``.

A context is passed to each template for it render just as with the dynamic template engine. The
main difference is that static template rendering does not occur in the context of a request, so
there is no request object to build context off of. Dynamic templates are also often rendering
contextual data built from the database but static templates are only rendered at deployment time,
so stuffing dynamic database information in static template contexts is not advisable.

Context configuration parameters may be any of the following:

    - **dictionary**: Simply specify context dictionary inline
    - **callable**: That returns a dictionary. This allows lazy context initialization to take
      place after Django bootstrapping
    - **json**: A path to a JSON file
    - **yaml**: A path to a YAML file (yaml supports comments!)
    - **pickle**: A path to a python pickled dictionary
    - **python**: A path to a python file. The locals defined in the file will
      comprise the context.
    - **a packaged resource**: Any of the above files imported as a packaged resource via
      :ref:`resource` to any of the above files.
    - **import string**: to any of the above.

For example:

.. code-block:: python

      from render_static import resource
      STATIC_TEMPLATES = {
        'context': resource('package.module', 'context.yaml')
      }


``templates``
-------------

The ``templates`` dictionary lists all templates that should be generated when `renderstatic` is
run with no arguments. If specific configuration directives including rendered path and context are
needed for a template they must be specified here.

.. note::

    `renderstatic` will be able to generate templates not listed in ``templates``, but only if
    supplied by name on the command line. Contexts may also be augmented/overridden via the command
    line.

``dest``
~~~~~~~~

Override the default destination where a template will be rendered. Templates loaded from ``DIRS``
instead of apps do not have a default destination and must be provided one here. When rendering a
single template, if the ``dest`` parameter is not an existing directory, it will be assumed to be
the full path including the file name where the template will be rendered. When rendering in batch
mode, ``dest`` will be treated as a directory and created if it does not exist.

``context``
~~~~~~~~~~~

Provide additional parameters for each template in the ``context`` dictionary. Any context variables
specified here that clash with global context variables will override them. May be specified using
any of the same context specifiers that work for the global context.


``RENDER_STATIC_REVERSAL_LIMIT``
--------------------------------

The guess and check reversal mechanism used to ensure that `urls_to_js` produces the same reversals
as Django's `reverse` is an **O(n^p)** operation where **n** is the number of placeholder candidates
to try and **p** is the number of arguments in the url. Its possible for this to produce a
complexity explosion for rare cases where the URL has a large number of arguments with unregistered
placeholders. A limit on the number of tries is enforced to guard against this. User's may adjust
the limit via the ``RENDER_STATIC_REVERSAL_LIMIT`` settings parameter. By default it is 2**14 tries
which runs in ~seconds per URL.

The solution if this limit is hit, is to provide more specific placeholders as placeholders are
attempted in order of specificity where specificity is defined by url name, variable name,
app name and/or converter type.
