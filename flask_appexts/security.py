# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppExts
# Copyright (C) 2015 CERN.
#
# Flask-AppExts is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask-Security extension.

You should set the following variables:

- SECURITY_CONFIRM_SALT
- SECURITY_DATASTORE_FACTORY
- SECURITY_EMAIL_SENDER
- SECURITY_EMAIL_SUBJECT_REGISTER
- SECURITY_LOGIN_SALT
- SECURITY_PASSWORD_SALT
- SECURITY_REMEMBER_SALT
- SECURITY_RESET_SALT
"""

from __future__ import print_function, absolute_import, unicode_literals

from celery import shared_task
from flask_wtf import RecaptchaField
from flask_security import Security
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from werkzeug.utils import import_string
from flask_appexts.mail import mail


security = Security()


#
# Forms
#
class RecaptchaFormMixin(object):

    """Recaptcha form mixin."""

    recaptcha = RecaptchaField()


class RecaptchaRegisterForm(RegisterForm, RecaptchaFormMixin):

    """Register form with recaptcha support."""


class RecaptchaConfirmRegisterForm(ConfirmRegisterForm, RecaptchaFormMixin):

    """Confirm register form with recaptcha support."""

    recaptcha = RecaptchaField()


#
# App setup
#
def setup_app(app):
    """Initialize Flask-Security."""
    app.config.setdefault('SECURITY_CHANGEABLE', True)
    app.config.setdefault('SECURITY_CONFIRMABLE', True)
    app.config.setdefault('SECURITY_DATASTORE_FACTORY', None)
    app.config.setdefault('SECURITY_PASSWORD_HASH', 'pbkdf2_sha512')
    app.config.setdefault('SECURITY_RECAPTCHA', True)
    app.config.setdefault('SECURITY_RECOVERABLE', True)
    app.config.setdefault('SECURITY_REGISTERABLE', True)
    app.config.setdefault('SECURITY_TRACKABLE', True)
    app.config.setdefault('SECURITY_LOGIN_WITHOUT_CONFIRMATION', True)

    # Get datastore factory method
    create_datastore = import_string(app.config.get(
        'SECURITY_DATASTORE_FACTORY'))

    if create_datastore is None:
        raise RuntimeError("Please specify SECURITY_DATASTORE_FACTORY")

    datastore = create_datastore(app)

    # Add recaptcha support if enabled.
    forms = {}
    if app.config['SECURITY_RECAPTCHA']:
        forms.update(dict(
            confirm_register_form=RecaptchaConfirmRegisterForm,
            register_form=RecaptchaRegisterForm,
        ))

    # Init extension.
    state = security.init_app(
        app,
        datastore=datastore,
        **forms
    )

    # TODO FIX celery
    celery = app.extensions['flask-celeryext'].celery

    @celery.task
    def send_security_email(msg):
        """Celery task to send security email."""
        mail.send(msg)

    # Use Celery task for sending emails.
    @state.send_mail_task
    def delay_security_email(msg):
        send_security_email.delay(msg)
