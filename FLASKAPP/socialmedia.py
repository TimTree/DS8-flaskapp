"""Retrieve messages, embeddings, and save to database"""

import basilica
from decouple import config
from .models import DB, Message, User
from .twitter_scraper import Profile, get_tweets

BASILICA = basilica.Connection(config('BASILICA_KEY'))