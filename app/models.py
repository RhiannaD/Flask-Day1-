from app import db,login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash


# class Team(db.Model):
#     id= db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     poke_id= db.Column(db.Integer, db.ForeignKey('poke.id'))
#     pokemons= db.relationship('Poke', backref='team', lazy='select')
#     user = db.relationship('User', backref='team', lazy='select')

team = db.Table(
    'team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_name', db.String, db.ForeignKey('poke.poke_name'))
)

class Poke(db.Model):
    poke_name =db.Column(db.String, primary_key=True)
    poke_ability = db.Column(db.String)
    poke_hp = db.Column(db.String)
    poke_defense = db.Column(db.String)
    poke_attack = db.Column(db.String)
    poke_image = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    def from_poke_dict(self, poke_data):
        self.poke_name = poke_data['name']
        self.poke_ability = poke_data['ability']
        self.poke_hp = poke_data['hp']
        self.poke_defense = poke_data['defense']
        self.poke_attack = poke_data['attack']
        self.poke_image = poke_data['image']


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password= db.Column(db.String)
    created_on= db.Column(db.DateTime, default =datetime.utcnow())
    team = db.relationship('Poke', secondary = team, backref='trainer',
     lazy='dynamic')
        
    def catch(self, poke):
        self.team.append(poke)
        db.session.commit()

    def release(self, poke):
        self.team.remove(poke)
        db.session.commit()

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
def load_user(id):
    return User.query.get(id)

