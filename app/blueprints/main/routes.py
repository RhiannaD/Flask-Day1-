from flask import request, render_template, redirect, url_for, flash
import requests
from app.blueprints.forms import PokeForm
from . import main
from flask_login import login_required, current_user
from app.models import User, db, Poke, team



@main.route('/home')
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/user/<username>')
def username(username):
    return f'Hello {username}!'





@main.route('/pokemon', methods=['GET','POST'])
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
            except IndexError:
        
                return "Bad request"
                
        
                
    return render_template('pokemon.html',form=form, poke_dict=poke_dict)


# catching route

@main.route('/catch/<poke_name>',methods=['GET','POST'])
@login_required
def catch(poke_name):
        query_poke= Poke.query.filter(Poke.poke_name == poke_name).first()
        query_user = User.query.get(team)
     
        
        url= f'https://pokeapi.co/api/v2/pokemon/{poke_name}'

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
            except IndexError:
            
                    return "Bad request"
                
            new_poke = Poke()
            new_poke.from_poke_dict(poke_dict)
            db.session.add(new_poke)
            db.session.commit()
            
            if query_user:
                current_user= User()
                current_user.catch(new_poke)


            if current_user.team == poke_name:
                 current_user.release(new_poke)
                
                
           

                 
            return redirect(render_template('profile.html', poke=poke))






# recieve a pokemon name
# 2. Query your database and see if that pokemon is in there
# 3. if it is, catch the pokemon current_user.catch(pokemon)
# using the info
# 5. then once you've added the pokemon to your database, catch th
                    


    # @main.route('/profile/<int:user_id>')
    # @login_required
    # def profile(user_id):
    #         user= User.query.get(user_id)
    #         if user:
    #             current_user.users_poke.append(user_id)
    #             db.session.commit()
    #             flash(f'Successfully followed {user.first_name}!', 'success')
    #             return redirect(url_for('main.profile'))
    #         else:
    #             flash('That user does not exist!', 'warning')
    #             return redirect(url_for('main.profile'))


