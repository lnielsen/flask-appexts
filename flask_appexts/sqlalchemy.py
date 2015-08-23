# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

""" extension."""

from __future__ import absolute_import, unicode_literals, print_function

import click
from flask_cli import with_appcontext
from flask.ext.sqlalchemy import SQLAlchemy
from flask_registry import ModuleAutoDiscoveryRegistry, RegistryProxy


db = SQLAlchemy()

models = RegistryProxy(
    'models',  # Registry namespace
    ModuleAutoDiscoveryRegistry,
    'models'   # Module name (i.e. models.py)
)


@click.group()
def database():
    """Database commands."""


@database.command()
@with_appcontext
def create():
    """Initialize database."""
    list(models)
    db.create_all()


def setup_app(app):
    """Initialize database extensions on application."""
    # Set default configuration
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db')
    # Add extension CLI to application.
    app.cli.add_command(database)
    db.init_app(app)
