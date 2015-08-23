# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-Collect extension."""

from __future__ import absolute_import, unicode_literals, print_function

import click
from flask_collect import Collect
from flask_cli import with_appcontext
from flask import current_app


@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True)
@with_appcontext
def collect(verbose=False):
    """Collect static files."""
    current_app.extensions['collect'].collect(verbose=verbose)


def setup_app(app):
    """Initialize Menu."""
    def filter_(items):
        """Filter application blueprints."""
        order = [blueprint.name for blueprint in
                 app.extensions['registry']['blueprints']]

        def _key(item):
            if item.name in order:
                return order.index(item.name)
            return -1

        return sorted(items, key=_key)

    app.config.setdefault('COLLECT_FILTER', filter_)
    app.config.setdefault('COLLECT_STATIC_ROOT', app.static_folder)

    ext = Collect(app)

    # unsetting the static_folder so it's not picked up by collect.
    class FakeApp(object):
        name = "fakeapp"
        has_static_folder = False
        static_folder = None

    ext.app = FakeApp()

    app.cli.add_command(collect)
