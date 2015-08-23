# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Admin extension."""

from __future__ import absolute_import, unicode_literals, print_function

from flask_admin import Admin

from flask_registry import ModuleAutoDiscoveryRegistry


class AdminDiscoveryRegistry(ModuleAutoDiscoveryRegistry):

    setup_func_name = 'setup_app'

    def register(self, module, *args, **kwargs):
        super(AdminDiscoveryRegistry, self).register(
            module, self.app, *args, **kwargs
        )


def setup_app(app):
    """Initialize Admin."""
    # Create registry and run discovery
    Admin(app, template_mode='bootstrap3')

    app.extensions['registry']['admin'] = AdminDiscoveryRegistry(
        'admin', app=app, with_setup=True)
