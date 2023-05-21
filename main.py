from flask import Flask, render_template, request
import requests
import json
import pandas as pd
import numpy as np

# Define the column names for the movie data
movie_columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date',
                 'imdb_url'] + ['unknown'] + ['0','1', '2', '3',
                                              '4', '5', '6', '7', '8', '9',
                                              '10', '11', '12', '13', '14', '15',
                                              '16', '17', '18']

# Load the movie data into a pandas DataFrame
movie_data = pd.read_csv('ml-100k/u.item', sep='|', names=movie_columns, encoding='latin-1')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        genre = request.form.get('genre')
        recommendations = recommend_movies(genre)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('home.html')

def get_movie_details(title, year):
    api_key = "89cdef23"  # replace with your OMDb API key
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}&y={year}&plot=short&r=json"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def recommend_movies(genre, n=3):
    # Filter the movies of the specified genre
    genre_movies = movie_data[movie_data[genre] == 1]
    
    # Select n random movies
    recommendations = genre_movies.sample(n)
    
    return recommendations['movie_title']

if __name__ == '__main__':
    app.run(debug=True)
