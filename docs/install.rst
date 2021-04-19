=======
Install
=======

.. note::

   Please note that this guide is not intended for production environments and
   is intended solely for local development.


Prerequisites
=============

To play with this blog at your local environment you need the following requirements:

* Python >= 3.7
* SQLite3
* sass
* npm

The project should work the same on the all major systems macOs, Linux or Windows (WSL)
and in general you don't need Docker, Nginx, RDBMS or VM to play with project at you local
environment.


Getting started
===============


Set up virtualenv
-----------------

.. code-block:: shell

   $ make init
   $ source .venv/bin/activate


Install dependencies
--------------------

.. code-block:: shell

   # For production server:
   $ pip install -r requirements/requirements.txt
   $ npm install

   # For local development:
   $ make install

To refresh dependencies in the future use the following approach:

.. code-block:: shell

   $ python -m pip install --upgrade pip-tools

   # For production server:
   $ rm requirements/requirements.txt
   $ make requirements/requirements.txt
   $ pip-sync requirements/requirements.txt

   # For local development:
   $ rm requirements/requirements-dev.txt
   $ make requirements/requirements-dev.txt
   $ pip-sync requirements/requirements-dev.txt


Create environment file
-----------------------

Copy ``settings.env.dist`` file to ``settings.env`` and make the
necessary changes:

.. code-block:: shell

   # Create configuration directory
   $ cp ./settings.env.dist ./settings.env


Run database migrations and create admin
----------------------------------------

   $ make migrate
   $ python manage.py createsuperuser


Load fixtures
-------------

.. code-block:: shell

   $ python manage.py loaddata settings.json
   $ python manage.py loaddata sites.json


Copy static files
-----------------

.. code-block:: shell

   $ make static

   # Also compile and compress css for production server:
   $ python manage.py compress


Run development server
----------------------

.. code-block:: shell

   # For local development only:
   $ make up


Final setup
-----------

Go to admin website and make the necessary changes in the following sections:

* ``/admin/sites/site``: Website domain and its name
* ``/admin/website/setting``: SEO, Google Analytics, Pagination, Color Scheme

Use value of the ``ADMIN_SITE_URL`` variable instead ``admin`` (see ``settings.env[.dist]``).
