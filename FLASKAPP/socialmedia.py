"""Retrieve messages, embeddings, and save to database"""

import basilica
from decouple import config
from .models import DB, Message, User
from .twitter_scraper import Profile, get_tweets

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """Add or update a user and their tweets, otherwise error"""
    try:
        twitter_user=username
        db_user=(User.query.get(int(Profile(twitter_user).userid)) or
        User(id=int(Profile(twitter_user).userid), name=username))
        DB.session.add(db_user)
        tweets = list(get_tweets(twitter_user, pages=5,include_rts=False))
        if tweets:
            db_user.newest_tweet_id = int(tweets[0]['tweetId'])
        for tweet in tweets:
            #calculate embedding on the full tweet
            embedding = BASILICA.embed_sentence(tweet['text'], model='twitter')
            db_message = Message(id=tweet['tweetId'], text=tweet['text'], embedding=embedding)
            DB.session.add(db_message)
            db_user.messages.append(db_message)
    except Exception as e:
        print('Error processing {}: {}'.format(username,e))
        raise e
    else:
        DB.session.commit()
