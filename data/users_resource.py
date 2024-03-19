from flask import jsonify
from flask_restful import Resource, abort
from . import db_session
from .users import User
from .reqparse import parser
from werkzeug.security import generate_password_hash
import datetime as dt


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"News {user_id} not found")


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'about', 'email', 'hashed_password', 'created_date'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'about', 'email', 'hashed_password', 'created_date')) for item in users]})


    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password']),
            created_date=dt.date
        )
        session.add(User)
        session.commit()
        return jsonify({'success': 'OK'})
