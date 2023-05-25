from flask import Flask, request, render_template
import requests 
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route('/home')
def home():
    return '<h1>This is the home page</h1>'

@app.route('/user/<username>')
def username(username):
    return f'Hello {username}!'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method== 'POST':
        return "Logged IN"
    else:
        return render_template('forms.html')
    
@app.route('/instructors')
def instructors():
    instructors_lst = ['Christian','Dylan','Sarah','Robert','Brendan']
    return render_template('instructors.html', instructors_lst=instructors_lst)

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    if request.method == 'POST':
        pokemon= request.form.get('pokemon')
        print(pokemon)
        url= f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
      
        poke = requests.get(url)
        print(poke)
        if poke.ok:
            poke_dict= {}
            try:
                data = poke.json()
                poke_ability= data["abilities"][0]["ability"]["name"]
                poke_name = data["forms"][0]["name"]
                poke_image = data["sprites"]["front_shiny"]
                poke_dict[poke_ability]={
                    "name": poke_name,
                    "image": poke_image
                }
                print(poke_dict)
                return render_template('pokemon.html', poke_dict=poke_dict)
            except IndexError:
                return "Bad request"
        
    return render_template('pokemon.html')





    