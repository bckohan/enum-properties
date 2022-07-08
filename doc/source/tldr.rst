.. _ref-usage:

=====
TL/DR
=====

First go back to the install page and install `django-render-static` if you haven't!

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


Your defines/model classes might look like this::

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
class their settings file might look like this::

    STATIC_TEMPLATES = {
        'templates': {
            'my_app/defines.js': {}
        }
    }

And then of course they would call :ref:`renderstatic` before `collectstatic`::

    $> ./manage.py renderstatic
    $> ./manage.py collectstatic

This would create the following file::

    .
    └── my_app
        └── static
            └── my_app
                └── defines.js

Which would look like this::

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

Your settings file might look like::

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

Then call :ref:`renderstatic` before `collectstatic`::

    $> ./manage.py renderstatic
    $> ./manage.py collectstatic

If your root urls.py looks like this::

    from django.contrib import admin
    from django.urls import include, path

    from .views import MyView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('simple', MyView.as_view(), name='simple'),
        path('simple/<int:arg1>', MyView.as_view(), name='simple'),
        path('different/<int:arg1>/<str:arg2>', MyView.as_view(), name='different'),
    ]

Then urls.js will look like this::

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

So you can now fetch paths like this::

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

.. warning::

    If you get an exception when you run :ref:`renderstatic` that originated from a
    :py:class:`render_static.exceptions.URLGenerationFailed` exception, you mostly likely need to
    register some :ref:`placeholders` before calling :ref:`urls_to_js`.

.. note::
    The JavaScript URL resolution is guaranteed to produce the same paths as Django's reversal
    mechanism. If it does not, this is a bug and we kindly ask
    `you to report it <https://github.com/bckohan/django-render-static/issues>`_.
