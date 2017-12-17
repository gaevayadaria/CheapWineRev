# -*- coding: utf-8 -*-

CSRF_ENABLED = True
SECRET_KEY = 'secret key hse'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# pagination
POSTS_PER_PAGE = 3

MAX_SEARCH_RESULTS = 50

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
SSL_DISABLE = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

NR_ADMIN = ['dariagaevaya@gmail.com>']
#NR_MAIL_SUBJECT_PREFIX = '[skv_newsreader]'
NR_MAIL_SENDER = 'newsReader Admin <dariagaevaya@gmail.com>'
