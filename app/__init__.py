# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

L_m = LoginManager()
L_m.init_app(app)
L_m.session_protection = 'strong'

mail = Mail(app)

from app import views, models
#db.drop_all()
#db.create_all()


