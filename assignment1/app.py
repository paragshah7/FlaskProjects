#!/usr/bin/env python
"""https://blog.miguelgrinberg.com/post/restful-authentication-with-flask"""

import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask import make_response
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy_utils import UUIDType
import uuid
import sqlalchemy

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


# SQLite Database
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True,
                         nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    account_created = db.Column(db.String, index=True, default=datetime.now)
    account_updated = db.Column(db.String, default=datetime.now)

    def hash_password(self, password):
        self.password_hash = Bcrypt().generate_password_hash(password).decode()

    def verify_password(self, password):
        return Bcrypt().check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['username'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/v1/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username, first_name=first_name,
                last_name=last_name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    response = jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'account_created': user.account_created,
        'account_updated': user.account_updated
    })
    response.status_code = 201
    return response
    # return (jsonify({'first_name': user.first_name, 'last_name': user.last_name}), 201,
    #         {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/v1/user/self', methods=['GET', 'PUT'])
@auth.login_required
def auth_api():
    if request.method == "GET":
        response = jsonify({
            'id': g.user.id,
            'first_name': g.user.first_name,
            'last_name': g.user.last_name,
            'username': g.user.username,
            'account_created': g.user.account_created,
            'account_updated': g.user.account_updated,
        })
        response.status_code = 200
        return response
    
    if request.method == "PUT":
        if request.json.get('username') is not None:
            return "Cannot modify username. Please supply first_name, last_name or password", 400
        if request.json.get('first_name') is not None:
            g.user.first_name = request.json.get('first_name')
        if request.json.get('last_name') is not None:
            g.user.last_name = request.json.get('last_name')
        if request.json.get('password') is not None:
            password = request.json.get('password')
            g.user.hash_password(password)
        g.user.account_updated = str(datetime.now())
        print(request.json)
        print(request.json.get('username'))
        print(request.json.get('username') is not None)
        db.session.add(g.user)
        db.session.commit()
        
        response = jsonify({
            'id': g.user.id,
            'first_name': g.user.first_name,
            'last_name': g.user.last_name,
            'account_created': g.user.account_created,
            'account_updated': g.user.account_updated,
        })
        response.status_code = 204
        return response



if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)

# Test Body
# POST = {"username":"parag3@gmail.com","password":"python3", "first_name":"parag3", "last_name":"shah3"}
# PUT = {"password":"python3", "first_name":"parag3", "last_name":"shah3"}
