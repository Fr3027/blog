from __future__ import print_function
import os
import sys
from flask_cors import CORS
from flask import Flask, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# def create_app(test_config=None):
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# g.db = db
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
# g.login_manager = login_manager
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


from app import auth,models
