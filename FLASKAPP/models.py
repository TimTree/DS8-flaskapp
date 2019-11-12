"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy

#import database. capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Social media users that we analyze"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

class Message(DB.Model):
    """The user's message from the social media site"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))