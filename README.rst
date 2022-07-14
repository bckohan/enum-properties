|MIT license| |PyPI version fury.io| |PyPI pyversions| |PyPI status| |Documentation Status|
|Code Cov| |Test Status|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/

.. |PyPI version fury.io| image:: https://badge.fury.io/py/django-render-static.svg
   :target: https://pypi.python.org/pypi/django-render-static/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/django-render-static.svg
   :target: https://pypi.python.org/pypi/django-render-static/

.. |PyPI status| image:: https://img.shields.io/pypi/status/django-render-static.svg
   :target: https://pypi.python.org/pypi/django-render-static

.. |Documentation Status| image:: https://readthedocs.org/projects/django-render-static/badge/?version=latest
   :target: http://django-render-static.readthedocs.io/?badge=latest/

.. |Code Cov| image:: https://codecov.io/gh/bckohan/django-render-static/branch/main/graph/badge.svg?token=0IZOKN2DYL
   :target: https://codecov.io/gh/bckohan/django-render-static

.. |Test Status| image:: https://github.com/bckohan/django-render-static/workflows/test/badge.svg
   :target: https://github.com/bckohan/django-render-static/actions

Enum-properties
#######################

Use Django's dynamic templates to render static files. That is, files that are collected
during the ``collectstatic`` routine and likely served above Django on the stack. Static
templates should be rendered preceding any run of ``collectstatic``. Files rendered by
django-render-static are immediately available to participate in the normal static file pipeline.

For example, a frequently occurring pattern that violates the DRY principle is the presence of
defines, or enum like structures in server side Python code that are simply replicated in client
side JavaScript. Single-sourcing these structures by generating client side code from the server
side code keeps the stack bone DRY.

`django-render-static` includes builtins for:
    - Replicating Django's `reverse` function in JavaScript (`urls_to_js`)
    - Auto-translating basic Python class and module structures into JavaScript
      (`modules_to_js`, `classes_to_js`)

You can report bugs and discuss features on the
`issues page <https://github.com/bckohan/django-render-static/issues>`_.

`Contributions <https://github.com/bckohan/django-render-static/blob/main/CONTRIBUTING.rst>`_ are
encouraged! Especially additional template tags and filters!

`Full documentation at read the docs. <https://django-render-static.readthedocs.io/en/latest/>`_

Installation
------------

1. Clone django-render-static from GitHub_ or install a release off PyPI_ :

.. code:: bash

       pip install django-render-static


2. Add 'render_static' to your ``INSTALLED_APPS`` :

.. code:: python

       INSTALLED_APPS = [
           'render_static',
       ]


3. Add a ``STATIC_TEMPLATES`` configuration directive to your settings file:

.. code:: python

        STATIC_TEMPLATES = {
            'templates' : {
                'path/to/template': {
                    'context' { 'variable': 'value' }
                }
        }


4. Run ``renderstatic`` preceding every run of ``collectstatic`` :

.. code:: bash

        $> manage.py renderstatic
        $> manage.py collectstatic


.. _GitHub: http://github.com/bckohan/django-render-static
.. _PyPI: http://pypi.python.org/pypi/django-render-static


Usage
-----

Generating Javascript Defines
-----------------------------

You have an app with a model with a character field that has several valid choices defined in an
enumeration type way, and you'd like to export those defines to JavaScript. You'd like to include
a template for other's using your app to use to generate a defines.js file. Say your app structure
looks like this::

    .
    └── my_app
        ├── __init__.py
        ├── apps.py
        ├── defines.py
        ├── models.py
        ├── static_templates
        │   └── my_app
        │       └── defines.js
        └── urls.py


Your defines/model classes might look like this:

.. code:: python

    class Defines:

        DEFINE1 = 'D1'
        DEFINE2 = 'D2'
        DEFINE3 = 'D3'
        DEFINES = (
            (DEFINE1, 'Define 1'),
            (DEFINE2, 'Define 2'),
            (DEFINE3, 'Define 3')
        )

    class MyModel(Defines, models.Model):

        define_field = models.CharField(choices=Defines.DEFINES, max_length=2)


And your defines.js template might look like this::

    var defines = {
        {{ "my_app.defines.Defines"|split|classes_to_js }}
    };


If someone wanted to use your defines template to generate a JavaScript version of your Python
class their settings file might look like this:

.. code:: python

    STATIC_TEMPLATES = {
        'templates': {
            'my_app/defines.js': {}
        }
    }


And then of course they would call `renderstatic` before `collectstatic`:

.. code:: bash

    $> ./manage.py renderstatic
    $> ./manage.py collectstatic


This would create the following file::

    .
    └── my_app
        └── static
            └── my_app
                └── defines.js

Which would look like this:

.. code:: javascript

    var defines = {
        Defines: {
            DEFINE1: 'D1'
            DEFINE2: 'D2'
            DEFINE3: 'D3'
            DEFINES: [
                ['D1', 'Define 1'],
                ['D2', 'Define 2'],
                ['D3', 'Define 3']
            ]
        }
    };


URL reverse functions
---------------------

You'd like to be able to call something like `reverse` on path names from your client JavaScript
code the same way you do from Python Django code. You don't want to expose your admin paths though.

Your settings file might look like:

.. code:: python

    from pathlib import Path

    BASE_DIR = Path(__file__).parent

    STATICFILES_DIRS = [
        BASE_DIR / 'more_static'
    ]

    STATIC_TEMPLATES = {
        'ENGINES': [{
            'BACKEND': 'render_static.backends.StaticDjangoTemplates',
            'OPTIONS': {
                'loaders': [
                    ('render_static.loaders.StaticLocMemLoader', {
                        'urls.js': (
                            '{% urls_to_js visitor="render_static.ClassURLWriter" '
                            'exclude=exclude %}'
                        )
                    })
                 ],
                'builtins': ['render_static.templatetags.render_static']
            },
        }],
        'templates': {
            'urls.js': {
                'dest': BASE_DIR / 'more_static' / 'urls.js',
                'context': {
                    'exclude': ['admin']
                }
            }
        }
    }


Then call `renderstatic` before `collectstatic`::

    $> ./manage.py renderstatic
    $> ./manage.py collectstatic

If your root urls.py looks like this:

.. code:: python

    from django.contrib import admin
    from django.urls import include, path

    from .views import MyView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('simple', MyView.as_view(), name='simple'),
        path('simple/<int:arg1>', MyView.as_view(), name='simple'),
        path('different/<int:arg1>/<str:arg2>', MyView.as_view(), name='different'),
    ]


Then urls.js will look like this:

.. code:: javascript

    class URLResolver {

        match(kwargs, args, expected) {
            if (Array.isArray(expected)) {
                return Object.keys(kwargs).length === expected.length &&
                    expected.every(value => kwargs.hasOwnProperty(value));
            } else if (expected) {
                return args.length === expected;
            } else {
                return Object.keys(kwargs).length === 0 && args.length === 0;
            }
        }

        reverse(qname, kwargs={}, args=[]) {
            let url = this.urls;
            for (const ns of qname.split(':')) {
                if (ns && url) { url = url.hasOwnProperty(ns) ? url[ns] : null; }
            }
            if (url) {
                let pth = url(kwargs, args);
                if (typeof pth === "string") { return pth; }
            }
            throw new TypeError(`No reversal available for parameters at path: ${qname}`);
        }

        urls = {
            "simple": (kwargs={}, args=[]) => {
                if (this.match(kwargs, args)) { return "/simple/"; }
                if (this.match(kwargs, args, ['arg1'])) { return `/simple/${kwargs["arg1"]}`; }
            },
            "different": (kwargs={}, args=[]) => {
                if (this.match(kwargs, args, ['arg1','arg2'])) {
                    return `/different/${kwargs["arg1"]}/${kwargs["arg2"]}`;
                }
            },
        }
    };


So you can now fetch paths like this:

.. code:: javascript

    // /different/143/emma
    const urls = new URLResolver();
    urls.reverse('different', {'arg1': 143, 'arg2': 'emma'});

    // reverse also supports query parameters
    // /different/143/emma?intarg=0&listarg=A&listarg=B&listarg=C
    url.reverse(
        'different',
        {
            kwargs: {arg1: 143, arg2: 'emma'},
            query: {
                intarg: 0,
                listarg: ['A', 'B', 'C']
            }
        }
    );


URLGenerationFailed Exceptions & Placeholders
---------------------------------------------

If you encounter a ``URLGenerationFailed`` exception, not to worry. You most likely need to register a placeholder for the argument in question. A placeholder is just a string or object that can be coerced to a string that matches the regular expression for the argument:

.. code:: python

   from render_static.placeholders import register_variable_placeholder

   app_name = 'year_app'
   urlpatterns = [
       re_path(r'^fetch/(?P<year>\d{4})/$', YearView.as_view(), name='fetch_year')
   ]

   register_variable_placeholder('year', 2000, app_name=app_name)

django-render-static avoids overly complex string parsing logic by reversing the urls and using the resultant regular expression match objects to determine where argument substitutions are made. This keeps the code simple, reliable and avoids deep dependencies on Django's url configuration code. Placeholders are the price paid for that reliability. Common default placeholders are attempted after all registered placeholders fail, and all of Django's native path converters are supported. This should allow most urls to work out of the box.

Users are **strongly** encouraged to use path instead of re_path and register their own custom converters when needed. Placeholders can be directly registered on the converter (and are then conveniently available to users of your app!):

.. code:: python

   from django.urls.converters import register_converter

   class YearConverter:
       regex = '[0-9]{4}'
       placeholder = 2000  # this attribute is used by `url_to_js` to reverse paths

       def to_python(self, value):
           return int(value)

       def to_url(self, value):
           return str(value)


   register_converter(YearConverter, 'year')

   urlpatterns = [
       path('fetch/<year:year>', YearView.as_view(), name='fetch_year')
   ]


