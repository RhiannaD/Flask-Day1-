from flask import request, render_template
import requests
from app.blueprints.forms import PokeForm
from . import main
from flask_login import login_required



@main.route('/home')
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/user/<username>')
def username(username):
    return f'Hello {username}!'

@main.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'




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
                # print(poke_dict)
                # return render_template('pokemon.html',form=form, poke_dict=poke_dict)
            
            except IndexError:
               
                return "Bad request"
        
                
    return render_template('pokemon.html',form=form, poke_dict=poke_dict)