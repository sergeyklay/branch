===============
Getting Started
===============

Installation
============

.. note::

  Some parts of this guide aren't intended for production usage and meant for
  local development only.


Prerequisites
-------------

To play with this blog at your local environment you need the following requirements:

* Python >= 3.7
* SQLite3
* `sass <https://sass-lang.com/install>`_
* npm

The project should work the same on the all major systems macOs, Linux or Windows (WSL)
and in general you don't need Docker, Nginx, RDBMS or VM to play with project at you local
environment. However, the following guide assumes that you are using Linux/Unix as a local
environment.


Set up virtualenv
-----------------

.. code-block:: shell

   $ python -m pip install --upgrade pip tox
   $ make init
   $ source .venv/bin/activate


Installing Dependencies
-----------------------

.. code-block:: shell

   # For production server:
   $ python -m pip install -r requirements/requirements.txt
   $ npm install

   # For local development:
   $ make install


To refresh dependencies in the future use the following approach:

.. code-block:: shell

   $ rm requirements/requirements.txt
   $ make requirements/requirements.txt
   $ pip-sync requirements/requirements.txt


Create environment file
-----------------------

Copy ``.env.dist`` file to ``.env`` and make the
necessary changes:

.. code-block:: shell

   # Create configuration directory
   $ cp ./.env.dist ./.env


Run database migrations and create admin
----------------------------------------

.. code-block:: shell

   $ make migrate
   $ python manage.py createsuperuser


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
   $ make serve
