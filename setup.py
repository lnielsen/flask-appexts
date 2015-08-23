# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-AppExts provide ready to use extensions for Flask-AppFactory."""

import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    """Integration of PyTest with setuptools."""

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        """Initialize options."""
        TestCommand.initialize_options(self)
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        config = ConfigParser()
        config.read("pytest.ini")
        self.pytest_args = config.get("pytest", "addopts").split(" ")

    def finalize_options(self):
        """Finalize options."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run tests."""
        # import here, cause outside the eggs aren't loaded
        import pytest
        import _pytest.config
        pm = _pytest.config.get_plugin_manager()
        pm.consider_setuptools_entrypoints()
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# Get the version string.  Cannot be done with import!
with open(os.path.join('flask_appexts', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read().replace('.. :changes:', '')

requirements = [
    'Flask-Registry',
    'Flask-AppFactory',
    'Flask-BabelEx',
    'Flask-Assets',
    'Flask-SQLAlchemy',
    'Flask-Security',
    'Flask-Mail',
    'Flask-Cache',
    'Flask-Menu',
    'Flask-Breadcrumbs',
    'Flask-DebugToolbar',
    'Flask-Session',
    'Flask-Collect',
    'Flask-Elasticsearch',
    'elasticsearch-dsl',
    'SQLAlchemy-Utils',
    'celery',
]

extras_requirements = {}

test_requirements = [
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.6.1',
    'coverage<4.0a1',
]

setup(
    name='Flask-AppExts',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    author="Invenio Collaboration",
    author_email='info@invenio-software.org',
    url='https://github.com/inveniosoftware/flask-appexts',
    packages=[
        'flask_appexts',
    ],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_requirements,
    license="BSD",
    zip_safe=False,
    keywords='flask-appexts',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
