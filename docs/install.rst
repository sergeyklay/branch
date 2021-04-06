=======
Install
=======


Prerequisites
=============

To play with this blog at your local environment you need the following requirements:

* macOs, Linux or Windows (WSL)
* Python >= 3.7
* SQLite3
* sass


Getting started
===============


Set up virtualenv
-----------------

.. code-block:: shell

   $ make init


Install dependencies
--------------------

.. code-block:: shell

   # For production server:
   $ pip install -r requirements/requirements.txt

   # For local development:
   $ pip install -r requirements/requirements-dev.txt

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
   $ sudo cp ./settings.env.dist ./settings.env


Load fixtures
-------------

.. code-block:: shell

   $ source .venv/bin/activate
   $ python manage.py loaddata ./provision/fixtures/01-settings.json


Copy static files
-----------------

.. code-block:: shell

   $ make static


Run development server
----------------------

.. code-block:: shell

   $ make up
