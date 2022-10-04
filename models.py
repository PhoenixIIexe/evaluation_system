from flask_login import UserMixin
from __init__ import db

from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    date = db.Column(db.DateTime())
    gender = db.Column(db.String(6))
    avatar = db.Column(db.String(100))
    publication = db.relationship('Publication', backref='user')
    comment = db.relationship('Comment', backref='user')

    __table_args__ = {'extend_existing': True}


class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(1000))
    comment = db.relationship('Comment', backref='publication')
    created_on = db.Column(db.DateTime(), default=datetime.now())

    __table_args__ = {'extend_existing': True}


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    text = db.Column(db.String(1000))
    created_on = db.Column(db.DateTime(), default=datetime.now())

    __table_args__ = {'extend_existing': True}
