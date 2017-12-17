# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from models import User


def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email is already used =(')


def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username is already used =(')
