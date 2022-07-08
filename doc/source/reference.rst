.. _ref-reference:

=========
Reference
=========

.. _engine:

engine
--------------------------------

.. automodule:: render_static.engine

   .. autoclass:: StaticTemplateEngine

.. _backends:

backends
----------------------------------

.. automodule:: render_static.backends

   .. autoclass:: StaticDjangoTemplates
   .. autoclass:: StaticJinja2Templates


.. _django_loaders:

loaders.django
---------------------------------

.. automodule:: render_static.loaders.django

   .. autoclass:: StaticAppDirectoriesLoader
   .. autoclass:: StaticFilesystemLoader
   .. autoclass:: StaticAppDirectoriesBatchLoader
   .. autoclass:: StaticFilesystemBatchLoader
   .. autoclass:: StaticLocMemLoader

.. _jinja2_loaders:

loaders.jinja2
---------------------------------

.. automodule:: render_static.loaders.jinja2

   .. autoclass:: StaticFileSystemLoader
   .. autoclass:: StaticFileSystemBatchLoader
   .. autoclass:: StaticPackageLoader
   .. autoclass:: StaticPrefixLoader
   .. autoclass:: StaticFunctionLoader
   .. autoclass:: StaticDictLoader
   .. autoclass:: StaticChoiceLoader
   .. autoclass:: StaticModuleLoader


.. _loader_mixins:

loaders.mixins
---------------------------------

.. automodule:: render_static.loaders.mixins

   .. autoclass:: BatchLoaderMixin

.. _origin:

origin
--------------------------------

.. automodule:: render_static.origin

   .. autoclass:: AppOrigin

.. _templatetags:

templatetags.django\_static\_templates
----------------------------------------------------------------

.. automodule:: render_static.templatetags.render_static

    .. autofunction:: split
    .. autofunction:: to_js
    .. autofunction:: classes_to_js
    .. autofunction:: modules_to_js
    .. autofunction:: urls_to_js

.. _exceptions:

exceptions
----------------------------------------------------------------

.. automodule:: render_static.exceptions

    .. autoclass:: URLGenerationFailed
    .. autoclass:: ReversalLimitHit


.. _placeholders:

placeholders
----------------------------------------------------------------

.. automodule:: render_static.placeholders

   .. autofunction:: register_converter_placeholder
   .. autofunction:: register_variable_placeholder
   .. autofunction:: register_unnamed_placeholders
   .. autofunction:: resolve_placeholders
   .. autofunction:: resolve_unnamed_placeholders


.. _javascript:

javascript
----------------------------------------------------------------

.. automodule:: render_static.javascript

   .. autoclass:: JavaScriptGenerator


.. _url_tree:

url_tree
----------------------------------------------------------------

.. automodule:: render_static.url_tree

   .. autoclass:: URLTreeVisitor
   .. autoclass:: SimpleURLWriter
   .. autoclass:: ClassURLWriter
   .. autoclass:: Substitute
   .. autofunction:: normalize_ns
   .. autofunction:: build_tree


.. _context:

context
----------------------------------------------------------------

.. automodule:: render_static.context

   .. autofunction:: resolve_context


.. _resource:

resource
----------------------------------------------------------------

.. automodule:: render_static.resource

   .. autofunction:: resource

