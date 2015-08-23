# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Registry for bundles."""

from __future__ import absolute_import, print_function, unicode_literals

from flask_assets import Bundle
from flask_registry import ModuleAutoDiscoveryRegistry
from werkzeug.utils import import_string


def register_bundles(app):
    """Register bundles in assets environment."""
    if 'bundles' not in app.extensions['registry']:
        app.extensions['registry']['bundles'] = \
            BundlesAutoDiscoveryRegistry(app=app)

    for name, bundle in app.extensions['registry']['bundles']:
        app.jinja_env.assets_environment.register(name, bundle)


class BundlesAutoDiscoveryRegistry(ModuleAutoDiscoveryRegistry):

    """Registry that searches for bundles.

    Its registry is a list of the package name and the bundle itself. This way
    you can keep track of where a bundle was loaded from.
    """

    def __init__(self, module_name=None, app=None, with_setup=False,
                 silent=False):
        """
        Initialize the bundle auto discovery registry.

        :param module_name: where to look for bundles (default: bundles)
        :type module_name: str

        """
        super(BundlesAutoDiscoveryRegistry, self).__init__(
            module_name or 'bundles', app=app, with_setup=with_setup,
            silent=silent)

    def _discover_module(self, module):
        """Discover the bundles in the given module."""
        import_str = module + '.' + self.module_name

        # FIXME this boilerplate code should be factored out in Flask-Registry.
        try:
            bundles = import_string(import_str, silent=self.silent)
        except ImportError as e:
            self._handle_importerror(e, module, import_str)
        except SyntaxError as e:
            self._handle_syntaxerror(e, module, import_str)
        else:
            variables = getattr(bundles, "__all__", dir(bundles))
            for var in variables:
                # ignore private/protected fields
                if var.startswith('_'):
                    continue
                bundle = getattr(bundles, var)
                if isinstance(bundle, Bundle):
                    self.register(("{0}:{1}".format(module, var),
                                   bundle))
