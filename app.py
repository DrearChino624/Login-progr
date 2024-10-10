from flask import Flask
from utils.database import db
from models import User
from flask_login import LoginManager

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_development')

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login.login'  # Assuming 'login' blueprint has a 'login' route

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all() 

# Import the user controller
from controllers import user_blueprint
app.register_blueprint(user_blueprint)

from controllers import login_blueprint
app.register_blueprint(login_blueprint)


if __name__ == "__main__":
    app.run(debug=True)

