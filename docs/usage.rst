=====
Usage
=====

CSS, Sass and compression
=========================

Using ``django-compressor``
---------------------------

Branch uses `django-compressor <https://django-compressor.readthedocs.io/en/stable/>`_ ,
an application that manages the compression pipeline for static files.

``django-compressor`` `offers several deployment modes <https://django-compressor.readthedocs.io/en/latest/scenarios/>`_:

1. **Offline Compression**: Compilation and compression is done manually once and for whole website
2. **In-Request Compression:** Compilation and compression is done automatically for each request

The first compression mode is suitable for deployment in production.
And the second one in a development environment.

.. warning::

   The second mode can significantly degrade performance and slow down work.

To use production ready compression mode, you'll need enable offline compression as follows:

.. code-block:: python

   # django.conf.settings.COMPRESS_OFFLINE
   COMPRESS_OFFLINE = True

It will then be necessary to manually start the compression if necessary:

.. code-block:: shell

   $ python manage.py compress

.. note::

   ``COMPRESS_OFFLINE`` is already set to ``True`` in ``branch.settings.prod`` module.
