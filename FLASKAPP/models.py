"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy

#import database. capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Social media users that we analyze"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    newest_message_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Message(DB.Model):
    """The user's message from the social media site"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(280))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref = DB.backref('messages',lazy=True))

    embedding = DB.Column(DB.PickleType, nullable=False)
    
    def __repr__(self):
        return '<Message {}>'.format(self.text)
