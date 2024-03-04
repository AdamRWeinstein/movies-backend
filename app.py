import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, url_for, redirect, flash
from flask_login import logout_user, login_user
from flask_cors import CORS
from flask_migrate import Migrate
from models import User
from extensions import db, bcrypt
import requests


load_dotenv()
api_key = os.environ.get('TMDB_API_KEY')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Login failed. Check email and password.'}), 401

@app.route('/logout')
def logout():
    logout_user()
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    user = User.register_user(username, email, password)
    
    if user:
        flash('User registered successfully.')
        return redirect(url_for('login'))
    else:
        flash('Registration failed.')
        return redirect(url_for('register'))


@app.route('/api/movies')
def get_recent_movies():
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    data = response.json()
    movie_results = data.get('results', [])
    return jsonify(movie_results)

if __name__ == '__main__':
    app.run(debug=True)
