# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Command-line tools for assets."""

from __future__ import print_function, absolute_import, unicode_literals


import json
import logging

import click
import pkg_resources
from flask import current_app
from flask_cli import with_appcontext

from .registry import register_bundles


def _webassets_cmd(cmd):
    """Helper to run a webassets command."""
    from webassets.script import CommandLineEnvironment
    register_bundles(current_app)
    logger = logging.getLogger('webassets')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(current_app.jinja_env.assets_environment,
                                    logger)
    getattr(cmdenv, cmd)()


@click.command()
@click.option("-i", "--bower-json", help="base input file", default=None,
              type=click.File('r'))
@click.option("-o", "--output-file", help="write bower.json to output file",
              metavar="FILENAME", type=click.File('w'))
@with_appcontext
def bower(bower_json, output_file):
    """Generate a bower.json file."""
    output = {
        "name": current_app.name,
        "version": pkg_resources.get_distribution(current_app.name).version,
        "dependencies": {},
    }

    if bower_json:
        output = dict(output, **json.load(bower_json))

    for imp, bundle in current_app.extensions['registry']['bundles']:
        if hasattr(bundle, 'bower'):
            output['dependencies'].update(bundle.bower)

    options = dict(indent=4)
    if output_file is None:
        click.echo(json.dumps(output, **options))
    else:
        json.dump(output, output_file, **options)


@click.group()
def assets():
    """Web assets commands."""


@assets.command()
@with_appcontext
def build():
    """Build bundles."""
    _webassets_cmd('build')


@assets.command()
@with_appcontext
def clean():
    """Clean bundles."""
    _webassets_cmd('clean')


@assets.command()
@with_appcontext
def watch():
    """Watch bundles for file changes."""
    _webassets_cmd('watch')


# parser.add_argument(
#             'bundles', nargs='*', metavar='BUNDLE',
#             help='Optional bundle names to process. If none are '
#                  'specified, then all known bundles will be built.')
#         parser.add_argument(
#             '--output', '-o', nargs=2, action='append',
#             metavar=('BUNDLE', 'FILE'),
#             help='Build the given bundle, and use a custom output '
#                  'file. Can be given multiple times.')
#         parser.add_argument(
#             '--directory', '-d',
#             help='Write built files to this directory, using the '
#                  'basename defined by the bundle. Will offset '
#                  'the original bundle output paths on their common '
#                  'prefix. Cannot be used with --output.')
#         parser.add_argument(
#             '--no-cache', action='store_true',
#             help='Do not use a cache that might be configured.')
#         parser.add_argument(
#             '--manifest',
#             help='Write a manifest to the given file. Also supports '
#                  'the id:arg format, if you want to use a different '
#                  'manifest implementation.')
#         parser.add_argument(
#             '--production', action='store_true',
#             help='Forcably turn off debug mode for the build. This '
#                  'only has an effect if debug is set to "merge".')
