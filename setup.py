# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

"""Setup module for Branch."""

import codecs
import re
from os import path

from setuptools import find_packages, setup


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'branch'
PKG_DIR = path.abspath(path.dirname(__file__))
META_PATH = path.join(PKG_DIR, PKG_NAME, '__init__.py')
META_CONTENTS = read_file(META_PATH)


def load_long_description():
    """Load long description from file README.rst."""
    def changes():
        changelog = path.join(PKG_DIR, 'CHANGELOG.rst')
        pat = r"(\d+.\d+.\d+ \(.*?\)\r?\n.*?)\r?\n\r?\n\r?\n----\r?\n\r?\n\r?\n"  # noqa: E501
        result = re.search(pat, read_file(changelog), re.S)

        return result.group(1) if result else ''

    try:
        title = f"{PKG_NAME}: {find_meta('description')}"
        head = '=' * (len(title) - 1)

        contents = (
            head,
            format(title.strip(' .')),
            head,
            read_file(path.join(PKG_DIR, 'README.rst')).split(
                '.. teaser-begin'
            )[1],
            '',
            read_file(path.join(PKG_DIR, 'CONTRIBUTING.rst')),
            '',
            'Release Information',
            '===================\n',
            changes(),
            '',
            f"`Full changelog <{find_meta('url')}/blob/master/CHANGELOG.rst>`_.",  # noqa: E501
            '',
            read_file(path.join(PKG_DIR, 'SECURITY.rst')),
            '',
            read_file(path.join(PKG_DIR, 'AUTHORS.rst')),
        )

        return '\n'.join(contents)
    except (RuntimeError, FileNotFoundError) as read_error:
        message = 'Long description could not be read from README.rst'
        raise RuntimeError(f'{message}: {read_error}') from read_error


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440."""
    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS."""
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        f'Unable to find __{meta}__ string in package meta file')


def get_version_string():
    """Return package version as listed in `__version__` in meta file."""
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


# What does this project relate to.
KEYWORDS = [
    'branch',
    'blog',
    'diary',
    'django',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Topic :: Internet',
    'Framework :: Django',
    'Framework :: Django :: 3.2',
    'Environment :: Web Environment',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',  # noqa: E501
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3 :: Only',
]

# Dependencies that are downloaded by pip on installation and why.
INSTALL_REQUIRES = [
    'celery[redis]>=5.0',  # Queues support
    'beautifulsoup4>=4.9.3',  # Sanitize HTML input
    'django>=3.2',  # Our framework
    'django-environ-2>=2.1.0',  # Configure Django application
    'django-compressor>=2.4',  # Compile and minify static assets
    'django-recaptcha>=2.0.6',  # reCAPTCHA support for Django
    'django-redis>=4.12.1',  # Redis cache backend for Django
    'gunicorn>=20.1.0',  # A Python WSGI HTTP Server
    'pillow>=8.2.0',  # Python Imaging Library
    'pyquery>=1.4.3',  # A jQuery-like Library for Python
]

DEPENDENCY_LINKS = []

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[develop,testing]
#
EXTRAS_REQUIRE = {
    # Dependencies that are required to run tests
    'testing': [
        'coverage[toml]>=5.0.2',  # Code coverage measurement for Python
        'pytest>=6.2.0',  # Our test framework
        'pytest-django>=4.2.0',  # A Django plugin for pytest
        'factory-boy>=3.2.0',  # A versatile test fixtures
        'faker>=8.1.0',  # A generator of fake data for tests
    ],
    # Dependencies that are required to build documentation
    'docs': []
}

# Dependencies that are required to develop package
DEVELOP_REQUIRE = [
    'django-debug-toolbar>=3.2',  # Django Debug Toolbar
    'django-extensions>=3.1.2',  # A collection of Django extensions
    'setuptools>=53.0.0',  # Build and install packages
    'wheel>=0.36.2',  # A built-package format for Python
]

EXTRAS_REQUIRE['develop'] = \
    DEVELOP_REQUIRE + EXTRAS_REQUIRE['testing'] + EXTRAS_REQUIRE['docs']

# Project's URLs
PROJECT_URLS = {
    'Changelog': f"{find_meta('url')}/blob/master/CHANGELOG.rst",
    'Bug Tracker': f"{find_meta('url')}/issues",
    'Source Code': f"{find_meta('url')}",
}

if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('author_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=load_long_description(),
        long_description_content_type='text/x-rst',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(exclude=['examples']),
        platforms=['any'],
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.7, <4',
        install_requires=INSTALL_REQUIRES,
        dependency_links=DEPENDENCY_LINKS,
        extras_require=EXTRAS_REQUIRE,
    )
