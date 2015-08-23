# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-Session extension."""

from __future__ import absolute_import, unicode_literals, print_function

from flask_session import Session


def setup_app(app):
    """Initialize Session."""
    if app.config.get('SESSION_TYPE'):
        Session(app)
