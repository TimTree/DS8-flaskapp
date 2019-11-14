from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .socialmedia import add_or_update_user
from .predict import predict_user

#now we make a app factory

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html',title='Homepage',users=users)

    # New route to add and get users
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, uimessage=''):
        name = name or request.values['user_name']
        try:
            if request.method=='POST':
                add_or_update_user(name)
                uimessage="User {} successfully added".format(name)
            messages = User.query.filter(User.name == name).one().messages
        except Exception as e:
            uimessage = "Error adding {}: {}".format(name,e)
            messages = []
        return render_template('user.html', title=name, messages=messages,uimessage=uimessage)

    @app.route('/compare', methods=['POST'])
    def compare(uimessage=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            uimessage = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            uimessage = '"{}" is more likely to be said by {} than {}'.format(
            request.values['tweet_text'], user1 if prediction else user2,
            user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', uimessage=uimessage)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html',title='Homepage',users=[])
    return app