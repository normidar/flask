#!/usr/bin/env python
import os
import time
from flask import Flask
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from apps import db, app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    character_id = db.Column(db.Integer)
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])

class Article(db.Model):
    __tablename__ = 'articles'
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(64), index=True)
    link_id = db.Column(db.Integer, index=True)
    owner   = db.Column(db.Integer,index=True)
    content = db.Column(db.String())
