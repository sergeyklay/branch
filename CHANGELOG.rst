Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.


1.3.0 (2021-XX-XX)
------------------

Features
^^^^^^^^

* Created SEO Tools as a standalone Django application.
* Provided ability to post HTML in the comments.
* Added Celery integration support.


Improvements
^^^^^^^^^^^^

* Provided language attribute for the main content of the page.
* Moved site name to the project's settings.
* Various minor improvements in semantic HTML.
* Improved meta description sanitizing.


Breaking Changes
^^^^^^^^^^^^^^^^

* Removed Django's sites integration as it no longer needed.
* Removed ``website`` application.
* All website settings have been moved to ``settings``.


Bug Fixes
^^^^^^^^^

* Fixed ``dc:`` meta tag definition.
* Fixed Email configuration to be able sent mails.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Bumped ``django`` from 3.2.1 to 3.2.2.


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
