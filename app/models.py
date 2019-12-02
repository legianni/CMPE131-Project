from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.Boolean, index=True)
    schedule = db.Column(db.String(
        350), index=True, default="[[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]]")
    events = db.relationship('Event', backref='author', lazy='dynamic')
    friends = db.relationship('Friend', backref='author', lazy='dynamic')
    friend_request = db.relationship(
        'FriendRequest', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(35), index=True)
    description = db.Column(db.String(256), index=True)
    date = db.Column(db.String(256), index=True)
    startTime = db.Column(db.String(256), index=True)
    endTime = db.Column(db.String(256), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}'.format(self.title)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friend_username = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Friend {}>'.format(self.id)


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_username = db.Column(db.String(64), index=True)
    friend_username = db.Column(db.String(64), index=True)
    request_status = db.Column(db.Boolean, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<FriendRequest {}>'.format(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
