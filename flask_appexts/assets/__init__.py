# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-Assets extension.

You should:

- Create a js/settings.js
- Add {% assets %} tags to your templates.

- myapp bower -o bower.json
- bower install
- myapp collect
- myapp assets build
"""

from __future__ import print_function, absolute_import, unicode_literals

from flask_assets import Environment

from .cli import assets as assets_cmd
from .cli import bower
from .registry import BundlesAutoDiscoveryRegistry, register_bundles
from .filters import RequireJSFilter, CleanCSSFilter
from .wrappers import BowerBundle

assets = Environment()


def setup_app(app):
    """Initialize assets extension.

    :param app: Flask application
    """
    app.extensions['registry']['bundles'] = \
        BundlesAutoDiscoveryRegistry(app=app)

    # Setup require.js variables.
    app.config.setdefault("REQUIREJS_BASEURL", app.static_folder)
    app.config.setdefault("REQUIREJS_CONFIG", 'js/settings.js')

    # Initialize extension
    assets.init_app(app)

    # Add CLI commands
    app.cli.add_command(assets_cmd)
    app.cli.add_command(bower)

    # Register bundles before first request
    app.before_first_request(lambda: register_bundles(app))
    return app


__all__ = (
    'assets', 'BowerBundle', 'CleanCSSFilter', 'register_bundles',
    'RequireJSFilter', 'setup_app',
)
