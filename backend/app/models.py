from __future__ import print_function
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import sys
from marshmallow_sqlalchemy import ModelSchema


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    print("id????", file=sys.stderr)
    print(id, file=sys.stderr)
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10))
    title = db.Column(db.String(20))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class PostSchema(ModelSchema):
    class Meta:
        model = Post
