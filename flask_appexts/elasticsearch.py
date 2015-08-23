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
from flask import current_app
from flask_elasticsearch import FlaskElasticsearch
from elasticsearch_dsl import Search
from werkzeug.local import LocalProxy
from flask_registry import ModuleAutoDiscoveryRegistry, RegistryProxy

es = FlaskElasticsearch()

search = LocalProxy(lambda: current_app.extensions['search'])

indexes = RegistryProxy(
    'indexes',  # Registry namespace
    ModuleAutoDiscoveryRegistry,
    'indexes'   # Module name (i.e. indexes.py)
)


def iter_doctypes():
    for module in indexes:
        for doctype in getattr(module, 'doctypes', []):
            yield doctype


def iter_indexes():
    for module in indexes:
        for idx in getattr(module, 'indexes', []):
            yield idx


@click.group()
def elasticsearch():
    """Elasticsearch commands."""


@elasticsearch.command()
@with_appcontext
def createindexes():
    """Initialize database."""
    for doctype in iter_doctypes():
        doctype.init(using=es)


def setup_app(app):
    """Initialize Elasticsearch."""
    es.init_app(app)
    app.extensions['search'] = Search().using(es)
    app.cli.add_command(elasticsearch)
