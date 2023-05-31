from app import db,login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash





class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password= db.Column(db.String)
    created_on= db.Column(db.DateTime, default =datetime.utcnow())

    # hashes our password when user signs up

    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)

    # this method will assign our columns eith their respective values

    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = self.hash_password(user_data['password'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)