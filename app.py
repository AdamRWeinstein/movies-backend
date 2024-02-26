import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import requests

load_dotenv()
api_key = os.environ.get('TMDB_API_KEY')

app = Flask(__name__)

@app.route('/api/movies')
def get_recent_movies():
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    data = response.json()
    movie_results = data.get('results', [])
    return jsonify(movie_results)

if __name__ == '__main__':
    app.run(debug=True)
