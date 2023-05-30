from flask import request, render_template,url_for,flash,redirect
import requests
from app.forms import LoginForm, SignUpForm,PokeForm
from app import app, db
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user,login_fresh,current_user,login_required,logout_user





@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<username>')
def username(username):
    return f'Hello {username}!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method== 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Welcome back {queried_user.first_name}!','success')
            return redirect(url_for('home'))
        else:
            error= 'Invalid email or password'
            return render_template('login.html', form=form, error=error)
    else:
        print("Not validated")
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_data={
            'first_name': form.first_name.data,
            'last_name' : form.last_name.data,
            'email' :form.email.data.lower(),
            'password' : form.password.data
        }

        # create user instance
        new_user = User()
        # set use_data to our User attributes
        new_user.from_dict(user_data)
        # save to database
        db.session.add(new_user)
        db.session.commit()


        flash(f'Thank you for signing up!{user_data["first_name"]}!', 'success')
        return redirect(url_for('login'))
    else:
        print("Invalid email or password", 'danger')
        return render_template('signup.html', form=form)
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!','warning')
    return redirect(url_for('home'))


@app.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokeForm()
    poke_dict={}
    if request.method == 'POST' and form.validate_on_submit():  
        pokemons = form.poke_name.data.lower()
        print(pokemons)
        url= f'https://pokeapi.co/api/v2/pokemon/{pokemons}'

        poke = requests.get(url)
       
       
        if poke.ok:
            try:
                data = poke.json()
                poke_ability= data["abilities"][0]["ability"]["name"]
                poke_name = data["forms"][0]["name"]
                poke_image = data["sprites"]["front_shiny"]
                poke_hp = data["stats"][0]["base_stat"]
                poke_defense= data["stats"][1]["base_stat"]
                poke_attack = data["stats"][2]["base_stat"]
                poke_dict ={
                    "name": poke_name,
                    "image": poke_image,
                    "ability": poke_ability,
                    "hp": poke_hp,
                    "defense": poke_defense,
                    "attack": poke_attack
    
                }
                # print(poke_dict)
                # return render_template('pokemon.html',form=form, poke_dict=poke_dict)
            
            except IndexError:
               
                return "Bad request"
        
                
    return render_template('pokemon.html',form=form, poke_dict=poke_dict)





    