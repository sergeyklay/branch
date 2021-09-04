Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

Improvements
^^^^^^^^^^^^

* Lowercase models verbose names.


----


1.5.0 (2021-09-03)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Renamed ``branch.settings.BASE_URL`` to ``branch.settings.SITE_URL``.
* Renamed ``branch.settings.BRANCH_LANGUAGES`` to ``branch.settings.SUPPORTED_LANGUAGES``.
* Removed ``apps.core.utils.admin_path`` in favor of ``branch.settings.ADMIN_SITE_URL``.


Features
^^^^^^^^

* Tune up comments page on admin site.
* Provided ``storage`` directory to store logs, coverage reports and so on.
* Provided custom command to make messages.
* Enabled log warnings on debug mode.
* Force the I18N machinery to always choose
  - ``branch.settings.SITE_LANGUAGE_CODE`` for the main site
  - ``branch.settings.ADMIN_LANGUAGE_CODE`` for the admin site
  as the default initial language unless another one is set via
  sessions or cookies.
* Setup ``branch.settings.ADMINS`` and ``branch.settings.MANAGERS`` to get
  system notifications.
* Provided ability to publish and unpublish selected comments.
* Adding the tagging functionality.


Improvements
^^^^^^^^^^^^

* Configured ``celery`` to use the same time zone as the app.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Returned to ``virtualenvwrapper`` for local development.
* Bumped ``prismjs`` from 1.23.0 to 1.24.1.
* Bumped ``trumbowyg`` from 2.24.0 to 2.25.1.
* Bumped ``faker`` from 8.11.0 to 8.12.1.
* Bumped ``pylint`` from 2.9.6 to 2.10.2.
* Bumped ``django`` from 3.2.6 to 3.2.7.
* Bumped ``django-environ-2`` from 2.1.0 to 2.2.0.
* Bumped ``pytest`` from 6.2.4 to 6.2.5.


----


1.4.0 (2021-06-25)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Renamed ``settings.env`` to ``.env``.
* Removed ``BRANCH_ENV`` env var as no longer used.
* The ``DJANGO_SETTINGS_MODULE`` env now points to ``branch.settings``.
* Refactor Django settings to follow twelve-factor methodology so that now only
  one config file is used, and all differences between environments are set by
  environment variables.
* Remove no longer used ``branch.settings.ENVIRON_SETTINGS_FILE_PATH`` variable.
* Rename ``CACHES_DEFAULT`` env var to ``CACHE_URL`` to use sane defaults.
* The ``BASE_DIR`` env var now is instance of ``pathlib.Path`` instead of ``environ.Path``.


Improvements
^^^^^^^^^^^^

* Changed additional groups of dependencies declared in ``setup.py`` so that
  ``develop`` is superset now for ``testing`` and ``docs``.
* Used single ``requirements.txt`` file to declare project dependencies.
  Additional dependencies from ``develop``, ``testing`` and ``docs`` groups
  lives now in ``setup.py`` or ``tox.ini``.


Bug Fixes
^^^^^^^^^

* Fixed Celery timezone configuration.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Migrate to tox.
* Migrated from ``django-environ`` to ``django-environ-2``.
* Bumped ``django`` from 3.2.3 to 3.2.4.
* Bumped ``django-redis`` from 4.12.1 to 5.0.0.
* Bumped ``click-repl`` from 0.1.6 to 0.2.0.
* Replaced ``pytest-cov`` by ``coverage[toml]`` for code coverage measurement.
* Bumped ``trumbowyg`` from 2.23.0 to 2.24.0.
* Bumped ``prompt-toolkit`` from 3.0.18 to 3.0.19.
* Bumped ``celery[redis]`` from 5.0.5 to 5.1.1.


----


1.3.0 (2021-05-21)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Removed Django's sites integration as it no longer needed.
* Removed ``website`` application.
* All website settings have been moved to ``settings``.


Features
^^^^^^^^

* Created SEO Tools as a standalone Django application.
* Provided ability to post HTML in the comments.
* Added Celery integration support.
* Contact form submission now uses Celery queues.
* Added reCAPTCHA v3 support.
* Added ``pyquery`` to perform queries for XML/HTML nodes.
* Added ``flake8-docstrings`` to check the content of Python docstrings for
  respect of the PEP 257.


Improvements
^^^^^^^^^^^^

* Provided language attribute for the main content of the page.
* Moved site name to the project's settings.
* Various minor improvements in semantic HTML.
* Improved meta description sanitizing.
* Reworked feeds to get rid of no longer used Sites module, improve items
  description and fix feeds URL.


Bug Fixes
^^^^^^^^^

* Fixed ``dc:`` meta tag definition.
* Fixed Email configuration to be able sent mails.
* Fixed contact form required fields.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Moved ``branch.models.AbstractPage`` to ``apps.core.models.Content``.
* Bumped ``django`` from 3.2.1 to 3.2.3.
* Bumped ``faker`` from 8.1.2 to 8.2.0.
* Bumped ``flake8`` from 3.9.1 to 3.9.2.
* Bumped ``pytest-cov`` from 2.11.1 to 2.12.0.
* Bumped ``pytest-django`` from 4.2.0 to 4.3.0.


----


1.2.0 (2021-05-04)
------------------


Features
^^^^^^^^

* Created a route to handle ``/robots.txt`` requests.
* Created a route to handle ``/humans.txt`` requests.
* Created Trumbowyg Editor as a standalone Django application.
* Implemented 500 error handler.
* Provided command to generate project's build ids.
* Provided caching configuration fro the project.
* Provided a way to configure site URL.


Improvements
^^^^^^^^^^^^

* Refactor 404 handler and move it to ``core`` app.


Bug Fixes
^^^^^^^^^

* Corrected ``dc:language`` meta tag definition for website pages.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Removed infrastructure configuration samples from the project repo.
* Corrected header format for ``setup.py --long-description``.
* Add ``django-redis`` to project requirements.
* Bumped ``django`` from 3.2.0 to 3.2.1.
* Bumped ``django-environ`` from 0.4.5 to ``develop`` branch to support secure redis connections.
* Bumped ``django-extensions`` from 3.1.2 to 3.2.3.
* Bumped ``pylint`` from 2.7.4 to 2.8.2.
* Bumped ``pylint-django`` from 2.4.3 to 2.4.4.
* Bumped ``pytest`` from 6.2.3 to 6.2.4.
* Bumped ``faker`` from 8.1.0 to 8.1.2.


----


1.1.0 (2021-04-19)
------------------


Features
^^^^^^^^

* Added ability to post and moderate comments.
* Added in-app logging support.
* Added Google Tag Manager support.
* Added RSS 2.0/Atom links to the page head.
* Provided ``apps.blog.models.Post.is_updated`` to see if
  the post has been updated since it was published.


Improvements
^^^^^^^^^^^^

* Optimized page speed by reorganizing static assets.
* Restructured and simplified template structure.
* Changed font families used on website to provide better reading experience:

  * Main font: PT Serif
  * Heading font: PT Sans


Bug Fixes
^^^^^^^^^

* Correct ``date_to_xmlschema`` template tag to not replace timezone


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Bumped ``django-debug-toolbar`` from 3.2 to 3.2.1.
* Bumped ``flake8`` from 3.9.0 to 3.9.1.
* Bumped ``django-compressor`` from 2.4 to 2.4.1.
* Removed incorrectly used and no longer needed ``ModelTimestampsMixin``.
* Rename field ``type`` on Post model to ``post_type`` to not shadow builtin.
* Added tests dependencies:

  * ``factory-boy==3.2.0``
  * ``faker==8.1.0``
  * ``flake8-blind-except==0.2.0``
  * ``flake8-builtins==1.5.3``
  * ``pylint-django==2.4.3``


----


1.0.0 (2021-04-14)
------------------

* Initial release.
