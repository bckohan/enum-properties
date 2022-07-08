.. _ref-installation:

============
Installation
============


1. Clone django-render-static from GitHub_ or install a release off PyPI_ ::

       pip install django-render-static


2. Add 'render_static' to your ``INSTALLED_APPS`` ::

       INSTALLED_APPS = [
           'render_static',
       ]

3. Add a ``STATIC_TEMPLATES`` configuration directive to your settings file::

        STATIC_TEMPLATES = {
            'templates' : {
                'path/to/template': {
                    'context' { 'variable': 'value' }
                }
        }

4. Run ``renderstatic`` preceding every run of ``collectstatic`` ::

        manage.py renderstatic
        manage.py collectstatic


.. _GitHub: http://github.com/bckohan/django-render-static
.. _PyPI: http://pypi.python.org/pypi/django-render-static
